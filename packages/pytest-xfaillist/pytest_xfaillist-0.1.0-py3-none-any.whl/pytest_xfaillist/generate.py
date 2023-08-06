from __future__ import annotations

import json
from codecs import open
from typing import TYPE_CHECKING

from . import config_to_xfaillist_path, item_to_test_id

if TYPE_CHECKING:
    from typing import Set

    from _pytest.config import Config
    from _pytest.python import Function
    from _pytest.runner import CallInfo

_faillist: Set[str] = set()


def pytest_runtest_makereport(item: Function, call: CallInfo[None]) -> None:
    if call.excinfo:
        _faillist.add(item_to_test_id(item))


def pytest_unconfigure(config: Config) -> None:
    path = config_to_xfaillist_path(config)
    with open(str(path), "w", encoding="UTF-8") as f:
        json.dump(list(_faillist), f, indent=4, sort_keys=True)
