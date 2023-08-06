import copy
import json
from dataclasses import dataclass
from typing import List, Optional, Union

import zipline.schema.thrift.ttypes as ttypes
from zipline.metadata_helper import get_dependencies, get_underlying_source

OperationType = int  # type(zthrift.Operation.FIRST)

#  The GroupBy's default online/production status is None and it will inherit
# online/production status from the Joins it is included.
# If it is included in multiple joins, it is considered online/production
# if any of the joins are online/production. Otherwise it is not online/production
# unless it is explicitly marked as online/production on the GroupBy itself.
DEFAULT_ONLINE = None
DEFAULT_PRODUCTION = None

# Fields allowed to be specified separated in streaming_query.
STREAMING_QUERY_FIELDS_ALLOWED = frozenset([
    'select',
    'where',
    'timeColumn',
])


@dataclass
class DefaultAggregation:
    operation: int = ttypes.Operation.LAST
    windows: Optional[List[ttypes.Window]] = None


def window_to_str_pretty(window: ttypes.Window):
    unit = ttypes.TimeUnit._VALUES_TO_NAMES[window.timeUnit].lower()
    return f"{window.length} {unit}"


def op_to_str(operation: OperationType):
    return ttypes.Operation._VALUES_TO_NAMES[operation].lower()


def _expand_aggregations(columns: List[str],
                         defaultAggregation: DefaultAggregation):
    """
    used to aggregate all the columns in the query using the same operation.
    """
    operation_name = op_to_str(defaultAggregation.operation)
    for column in columns:
        yield ttypes.Aggregation(
            name=f"{column}_{operation_name}",
            inputColumn=column,
            operation=defaultAggregation.operation,
            windows=defaultAggregation.windows,
        )


def Select(**kwargs):
    """
    Convenience function to convert kwargs into a map.
    A map from alias to expression is what the underlying thrift object expects
    """
    return kwargs


def Aggregations(**kwargs):
    """
    fills in missing arguments of the aggregation object.
    default operation is LAST
    default name is {arg_name}_{operation_name}
    default input column is {arg_name}
    """
    aggs = []
    for name, aggregation in kwargs.items():
        assert isinstance(aggregation, ttypes.Aggregation), \
            f"argument for {name}, {aggregation} is not instance of Aggregation"
        if not aggregation.name:
            aggregation.name = name
        if not aggregation.operation:  # Default operation is last
            aggregation.operation = ttypes.Operation.LAST
        if not aggregation.inputColumn:  # Default input column is the variable name
            aggregation.inputColumn = name
        aggs.append(aggregation)
    return aggs


def get_query(source: ttypes.Source):
    return get_underlying_source(source).query


def get_streaming_query(source: ttypes.Source):
    return get_underlying_source(source).streamingQuery


def get_columns(source: ttypes.Source):
    query = get_query(source)
    columns = query.select.keys()
    return columns


def contains_windowed_aggregation(aggregations: Optional[Union[List[ttypes.Aggregation], DefaultAggregation]]) -> bool:
    if not aggregations:
        return False
    if isinstance(aggregations, DefaultAggregation):
        if aggregations.windows:
            return True
    else:
        for agg in aggregations:
            if agg.windows:
                return True
    return False


def set_ts_as_time_column(query: ttypes.Query):
    query.select.update({"ts": query.timeColumn})


def get_topic(source: ttypes.Source) -> str:
    if source.events:
        return source.events.topic
    else:
        return source.entities.mutationTopic


def contains_realtime_source(sources: List[ttypes.Source]) -> bool:
    return any(get_topic(source) for source in sources)


def validate_streaming_query(query: ttypes.Query,
                              streaming_query: ttypes.Query):
    default_query = ttypes.Query()
    query_keys = query.select.keys()
    streaming_query_keys = streaming_query.select.keys()
    assert len(query_keys - streaming_query_keys) == 0, \
        "streaming query select keys ({}) and query select keys ({}) do not match".format(
            query_keys, streaming_query_keys)
    # nonempty field that has value different from default values.
    nonempty_field_keys = set([k for (k, v) in streaming_query.__dict__.items()
                               if v is not None and len(v) > 0
                               and getattr(default_query, k) != v])
    disallowed_keys = nonempty_field_keys - STREAMING_QUERY_FIELDS_ALLOWED
    assert len(disallowed_keys) == 0, \
        "streaming query cannot specify the following fields: {}".format(", ".join(disallowed_keys))


def validate_group_by(sources: List[ttypes.Source],
                      keys: List[str],
                      has_aggregations: bool,
                      is_realtime):
    # check ts is not included in query.select
    first_source_columns = set(get_columns(sources[0]))
    assert "ts" not in first_source_columns, "'ts' is a reserved key word for Zipline," \
                                             " please specify the expression in timeColumn"
    for src in sources:
        query = get_query(src)
        if src.events:
            assert query.ingestionTimeColumn is None, "ingestionTimeColumn should not be specified for " \
                                                      "event source as it should be the same with timeColumn"
            assert query.reversalColumn is None, "reversalColumn should not be specified for event source " \
                                                 "as it won't have mutations"
        if has_aggregations:
            assert query.timeColumn, "Please specify timeColumn for source's query with windowed aggregations"
        streaming_query = get_streaming_query(src)
        if streaming_query:
            validate_streaming_query(query, streaming_query)
        else:
            streaming_query = query
        if is_realtime:
            assert streaming_query.timeColumn, \
                "Please specify timeColumn for source's streaming query with realtime streaming enabled"

    # all sources should select the same columns
    for i, source in enumerate(sources[1:]):
        column_set = set(get_columns(source))
        column_diff = column_set ^ first_source_columns
        assert not column_diff, f"""
Mismatched columns among sources [1, {i+2}], Difference: {column_diff}
"""

    # all keys should be present in the selected columns
    unselected_keys = set(keys) - first_source_columns
    assert not unselected_keys, f"""
Keys {unselected_keys}, are unselected in source
"""


def GroupBy(sources: Union[List[ttypes.Source], ttypes.Source],
            keys: List[str],
            aggregations: Optional[Union[List[ttypes.Aggregation], DefaultAggregation]],
            user_var = None,
            online: bool = DEFAULT_ONLINE,
            production: bool = DEFAULT_PRODUCTION) -> ttypes.GroupBy:
    assert sources, "Sources are not specified"

    if isinstance(sources, ttypes.Source):
        sources = [sources]
    has_aggregations = contains_windowed_aggregation(aggregations)
    is_realtime = online and contains_realtime_source(sources)
    validate_group_by(sources, keys, has_aggregations, is_realtime)

    # create a deep copy for case: multiple group_bys use the same sources,
    # validation_sources will fail after the first group_by
    updated_sources = copy.deepcopy(sources)
    # mapping ts with query.timeColumn
    for src in updated_sources:
        query = get_query(src)
        streaming_query = get_streaming_query(src)
        if src.events:
            set_ts_as_time_column(query)
            if is_realtime and streaming_query:
                set_ts_as_time_column(streaming_query)
        # entity source
        elif query.timeColumn:
            # timeColumn for entity source is optional
            set_ts_as_time_column(query)
            if is_realtime and streaming_query:
                set_ts_as_time_column(streaming_query)

    query = get_query(updated_sources[0])
    columns = get_columns(updated_sources[0])
    expanded_aggregations = aggregations
    # expand default aggregation to actual aggregations
    if isinstance(aggregations, DefaultAggregation):
        # TODO: validate that all timeColumns and partitionColumns
        # are the same in all the sources
        # column names that need to be excluded from aggregation
        non_aggregate_columns = keys + [
            "ts",
            query.timeColumn,
            query.partitionColumn
        ]
        aggregate_columns = [
            column
            for column in columns
            if column not in non_aggregate_columns
        ]
        expanded_aggregations = list(_expand_aggregations(
            aggregate_columns,
            aggregations
        ))
    # flattening
    dependencies = [dep for source in updated_sources for dep in get_dependencies(source) ]
    metadata = json.dumps({"dependencies": dependencies})

    if user_var:
        metadata["user_json"] = json.dumps(user_var)

    return ttypes.GroupBy(
        sources=updated_sources,
        keyColumns=keys,
        aggregations=expanded_aggregations,
        metadata=metadata,
        online=online,
        production=production
    )
