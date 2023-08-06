import gc
import importlib
from collections.abc import Iterable
from typing import List

from zipline.group_by import GroupBy
from zipline.schema.thrift.ttypes import Source, EventSource, StagingQuery

# Required fields in check consistency select statement.
REQUIRED_CHECK_CONSITENCY_FIELDS = frozenset(['keys_json', 'values_json', 'timestamp'])


def edit_distance(str1, str2):
    m = len(str1) + 1
    n = len(str2) + 1
    dp = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],
                                   dp[i - 1][j],
                                   dp[i - 1][j - 1])
    return dp[m - 1][n - 1]


def check_contains_single(candidate, valid_items, type_name, name, print_function=repr):
    name_suffix = f"for {name}" if name else ""
    candidate_str = print_function(candidate)
    if not valid_items:
        assert f"{candidate_str}, is not a valid {type_name} because no {type_name}s are specified {name_suffix}"
    elif candidate not in valid_items:
        sorted_items = sorted(map(print_function, valid_items),
                              key=lambda item: edit_distance(candidate_str, item))
        printed_items = '\n    '.join(sorted_items)
        assert candidate in valid_items, f"""{candidate_str}, is not a valid {type_name} {name_suffix}
Please pick one from:
    {printed_items}
"""


def check_contains(candidates, *args):
    if isinstance(candidates, Iterable) and not isinstance(candidates, str):
        for candidate in candidates:
            check_contains_single(candidate, *args)
    else:
        check_contains_single(candidates, *args)


def get_streaming_sources(group_by: GroupBy) -> List[Source]:
    """Checks if the group by has a source with streaming enabled."""
    return [source for source in group_by.sources if is_streaming(source)]


def is_streaming(source: Source) -> bool:
    """Checks if the source has streaming enabled."""
    return (source.entities and source.entities.mutationTopic is not None) or \
        (source.events and source.events.topic is not None)


def import_module_set_name(module, cls):
    """evaluate imported modules to assign object name"""
    for name, obj in list(module.__dict__.items()):
        if isinstance(obj, cls):
            # the name would be `team_name.python_script_name.[group_by_name|join_name|staging_query_name]`
            # real world case: psx.reservation_status.v1
            obj.name = module.__name__.partition(".")[2] + "." + name
    return module


def get_mod_name_from_gc(obj, mod_prefix):
    """get an object's module information from garbage collector"""
    mod_name = None
    # get obj's module info from garbage collector
    gc.collect()
    for ref in gc.get_referrers(obj):
        if '__name__' in ref and ref['__name__'].startswith(mod_prefix):
            mod_name = ref['__name__']
            break
    return mod_name


def get_staging_query_output_table_name(staging_query: StagingQuery):
    """generate output table name for staging query job"""
    staging_query_module = importlib.import_module(get_mod_name_from_gc(staging_query, "staging_queries"))
    import_module_set_name(staging_query_module, StagingQuery)
    return staging_query.name.replace('.', '_')


def validate_check_consistency_source(check_consistency_source: EventSource) -> str:
    """Validate check_consistency_source object and returns error_msg if there is any errors.
    """
    if not isinstance(check_consistency_source, EventSource):
        return "check_consistency_source should be a EventSource object."
    if not check_consistency_source.table:
        return "check_consistency_source should have table."
    if not check_consistency_source.query or not check_consistency_source.query.select:
        return "check_consistency_source must have query with select."
    keys_not_present = check_consistency_source.query.select.keys() - \
        REQUIRED_CHECK_CONSITENCY_FIELDS
    if keys_not_present:
        keys_not_present_str = ", ".join(keys_not_present)
        return f"required fields {keys_not_present} are not present in Select."
