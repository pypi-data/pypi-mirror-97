from typing import Dict, Union, Set, List

import os
import sys


def increment_counter(d: Dict[str, int], key: str) -> None:
    if key in d:
        d[key] += 1
    else:
        d[key] = 1


def ensure_str_decoded(s: Union[str, bytes]) -> str:
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s


def combine_value_lists(d: Dict[str, List[str]]) -> List[str]:
    result: Set[str] = set()
    for value_list in d.values():
        result = result.union(set(value_list))
    return sorted(result)


def get_module_name_from_path(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]


def is_valid_mypy_path_entry(path_entry: str) -> bool:
    """
    We try to configure MYPYPATH to be the same as PYTHONPATH, but without any site-packages
    directories. Otherwise, mypy gives us the following message:

    .../site-packages is in the MYPYPATH. Please remove it.
    See https://mypy.readthedocs.io/en/latest/running_mypy.html#how-mypy-handles-imports for
    more info.

    Also we don't allow other system-wide module paths there.
    """
    return (
        os.path.basename(path_entry) != 'site-packages' and
        '/site-packages/' not in path_entry and
        # macOS-specific
        '/Library/Frameworks/Python.framework/' not in path_entry
    )


def get_sys_path_entries_for_mypy() -> List[str]:
    return [
        sys_path_entry for sys_path_entry in sys.path
        if is_valid_mypy_path_entry(sys_path_entry)
    ]
