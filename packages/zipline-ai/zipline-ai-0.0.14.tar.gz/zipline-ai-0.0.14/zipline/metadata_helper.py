import re
import zipline.schema.thrift.ttypes as ttypes
from typing import List, Dict, Union


def get_underlying_source(source: ttypes.Source):
    return source.entities if source.entities else source.events


def construct_dependencies(table: str, query: ttypes.Query) -> List[Dict[str, Union[int, str]]]:
    date_part = query.partitionColumn
    deps = query.dependencies
    ds_string = "{{ ds }}"

    if deps:
        result = [{
            "name": re.sub('_+', '_', f"wait_for_{table}_{re.sub('[^a-zA-Z0-9]', '_', dep)}").rstrip('_'),
            "spec": dep,
            "start": query.startPartition,
            "end": query.endPartition
        } for dep in deps]
    else:
        result = [{
            "name": f"wait_for_{table}_{date_part}",
            "spec": f"{table}/{date_part}={ds_string}",
            "start": query.startPartition,
            "end": query.endPartition
        }]
    return result


def get_dependencies(source: ttypes.Source) -> List[Dict]:
    inner_source = get_underlying_source(source)
    query = inner_source.query
    base_table = source.entities.snapshotTable if source.entities else source.events.table

    dependencies = construct_dependencies(base_table, query)
    return dependencies
