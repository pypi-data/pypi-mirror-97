import copy
import importlib
import json
import logging
import re
from typing import List, Dict, Union, Optional, Iterable

import zipline.group_by as gb
import zipline.schema.thrift.ttypes as ttypes
import zipline.utils as utils
from zipline.metadata_helper import get_dependencies
from zipline.schema.serializer import thrift_simple_json

logging.basicConfig(level=logging.INFO)

# Regex for matching table name in check_conistency args in LeftOuterJoin.
TABLE_NAME_REGEX = re.compile(r"^\w+\.\w+$")

def _expand_selectors(group_by: ttypes.GroupBy,
                      selectors: Optional[List[Union[ttypes.AggregationSelector, str]]]):
    if selectors is None:
        if group_by.aggregations:
            for aggregation in group_by.aggregations:
                if aggregation.windows:
                    yield ttypes.AggregationSelector(
                        name=aggregation.name,
                        windows=aggregation.windows
                    )
                else:
                    yield ttypes.AggregationSelector(
                        name=aggregation.name
                    )
        else:
            for column in gb.get_columns(group_by.sources[0]):
                yield ttypes.AggregationSelector(name=column)
    else:
        valid_names: Optional[Iterable[str]] = None
        aggregation_map: Dict[str, ttypes.Aggregation]
        if group_by.aggregations:
            aggregation_map = {
                aggregation.name: aggregation
                for aggregation in group_by.aggregations
            }
            valid_names = aggregation_map.keys()
        else:  # pre-aggregated
            valid_names = set([column for column in gb.get_columns(group_by.sources[0])])
        for selector in selectors:
            if isinstance(selector, ttypes.AggregationSelector):
                utils.check_contains(selector.name,
                                     valid_names,
                                     "aggregation",
                                     group_by.name)
                if selector.windows:
                    assert group_by.aggregations, f"""
group_by:{group_by.name} doesn't have windows, and is pre-aggregated.
You requested: {selector}
"""
                    utils.check_contains(selector.windows,
                                         aggregation_map[selector.name].windows,
                                         "window",
                                         f"{group_by.name}:{selector.name}",
                                         gb.window_to_str_pretty)
                yield selector
            else:
                # selector is a string name
                utils.check_contains(selector, valid_names, "aggregation", group_by.name)
                yield ttypes.AggregationSelector(
                    name=selector
                )


def JoinPart(group_by: ttypes.GroupBy,
             keyMapping: Dict[str, str] = None,  # mapping of key columns from the join
             selectors: Optional[List[Union[ttypes.AggregationSelector, str]]] = None,
             prefix: str = None  # all aggregations will be prefixed with that name
             ) -> ttypes.JoinPart:
    # used for reset for next run
    import_copy = __builtins__['__import__']
    group_by_module_name = utils.get_mod_name_from_gc(group_by, "group_bys")
    logging.debug("group_by's module info from garbage collector {}".format(group_by_module_name))
    group_by_module = importlib.import_module(group_by_module_name)
    __builtins__['__import__'] = utils.import_module_set_name(group_by_module, ttypes.GroupBy)
    if keyMapping:
        utils.check_contains(keyMapping.values(),
                             group_by.keyColumns,
                             "key",
                             group_by.name)

    join_part = ttypes.JoinPart(
        groupBy=group_by,
        keyMapping=keyMapping,
        selectors=list(_expand_selectors(group_by, selectors)),
        prefix=prefix
    )
    # reset before next run
    __builtins__['__import__'] = import_copy
    return join_part


def LeftOuterJoin(left: ttypes.Source,
                  rightParts: List[ttypes.JoinPart],
                  check_consistency: bool = False,
                  check_consistency_table: str = "",
                  check_consistency_source: ttypes.EventSource = None,
                  additional_args: List[str] = None,
                  additional_env: List[str] = None,
                  user_var = None,
                  online: bool = False,
                  production: bool = False) -> ttypes.LeftOuterJoin:
    """
    defines the primary keys and timestamps for which Zipline is to compute
    features and a list of Aggregations to combine into a single data source
    (usually for training data).

    Note: users can only set one of consistency_check, consistency_check_table,
    and consistency_check_source option.

    :param left: The primary keys and timestamps for the driver.
    :param rightParts: a list of JoinParts(aggregations) to select.
    :param consistency_check: If True, default Zipline online offline consistency check is used.
    :param check_conistency_table: If set, table name in the format of
           <namespace>.<table> will  be used in online offline consistency check.
    :param consistency_check_source: If set as EventSource, its table and query
           with select keys_json, values_json, timestamp will be used to run
           consistency_check_source.
    :param additional_args: Additional args passed to JoinJob.
    :param additional_env: Additional environment variable passed to Spark submit.
    :param user_var: users can assign any variables and later be json serialized to the metadata
    :param online: Set to true if the Join is served online.
    :param production: Set to true if the Join is used in the production environment.
    """
    # create a deep copy for case: multiple LeftOuterJoin use the same left,
    # validation will fail after the first iteration
    updated_left = copy.deepcopy(left)
    if left.events:
        if left.events.query.select:
            assert "ts" not in left.events.query.select.keys(), "'ts' is a reserved key word for Zipline," \
                                                              " please specify the expression in timeColumn"
            # mapping ts to query.timeColumn to events only
            updated_left.events.query.select.update({"ts": updated_left.events.query.timeColumn})

    # name is set externally, cannot be set here.
    root_base_source = updated_left.entities if updated_left.entities else updated_left.events
    # todo: validation if select is blank
    if root_base_source.query.select:
        root_keys = set(root_base_source.query.select.keys())
        # JoinJob will compute a 128 bit row hash as the row_id
        assert "row_id" not in root_keys, "'row_id' is a reserved key word for Zipline"
        for joinPart in rightParts:
            mapping = joinPart.keyMapping if joinPart.keyMapping else {}
            utils.check_contains(mapping.keys(), root_keys, "root key", "")
            uncovered_keys = set(joinPart.groupBy.keyColumns) - set(mapping.values()) - root_keys
            assert not uncovered_keys, f"""
    Not all keys columns needed to join with GroupBy:{joinPart.groupBy.name} are present.
    Missing keys are: {uncovered_keys},
    Missing keys should be either mapped or selected in root.
    KeyMapping only mapped: {mapping.values()}
    Root only selected: {root_keys}
            """

    dependencies = get_dependencies(updated_left)

    right_sources = [joinPart.groupBy.sources for joinPart in rightParts]
    # flattening
    right_sources = [source for source_list in right_sources for source in source_list]
    right_dependencies = [dep for source in right_sources for dep in get_dependencies(source)]

    dependencies.extend(right_dependencies)
    metadata_map = {
        "dependencies": json.dumps(list({frozenset(item.items()): item for item in dependencies}.values()))
    }

    if additional_args:
        metadata_map["additional_args"] = additional_args

    if additional_env:
        metadata_map["additional_env"] = additional_env

    if user_var:
        metadata_map["user_json"] = json.dumps(user_var)

    check_consistency_options = [
        'check_consistency', 'check_consistency_table', 'check_consistency_source']
    scope = locals()
    set_options = [option for option in check_consistency_options if eval(option, scope)]
    assert len(set_options) < 2, "only one of ({}) options must be set: {} are set".format(
        ", ".format(check_consistency_options), ", ".format(set_options))
    if check_consistency is True:
        metadata_map["check_consistency"] = "default"
    elif check_consistency_table:
        assert TABLE_NAME_REGEX.match(check_consistency_table), \
            f"check_consistency_table {check_consistency_table} is invalid table name"
        metadata_map["check_consistency_table"] = check_consistency_table
    if check_consistency_source:
        assert isinstance(check_consistency_source, ttypes.EventSource), \
            "check_consistency source should be a EventSource object."
        error_msg = utils.validate_check_consistency_source(check_consistency_source)
        assert not error_msg, f"check_consistency_source is invalid: {error_msg}"
        metadata_map["check_consistency_source"] = json.loads(
            thrift_simple_json(check_consistency_source))
    metadata = json.dumps(metadata_map)

    return ttypes.LeftOuterJoin(
        left=updated_left,
        rightParts=rightParts,
        metadata=metadata,
        online=online,
        production=production
    )
