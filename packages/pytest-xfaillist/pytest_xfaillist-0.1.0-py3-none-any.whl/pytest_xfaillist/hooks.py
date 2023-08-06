from __future__ import annotations

import json
from typing import TYPE_CHECKING

from _pytest.python import Function
from pytest import mark

from . import config_to_xfaillist_path, item_to_test_id

if TYPE_CHECKING:
    from typing import Set

    from _pytest.config import Config
    from _pytest.config.argparsing import Parser
    from _pytest.main import Session

_faillist: Set[str] = set()


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--generate-xfaillist", action="store_true", help="Generate xfail.list"
    )


def pytest_configure(config: Config):
    if config.option.generate_xfaillist:
        config.pluginmanager.import_plugin("pytest_xfaillist.generate")
    else:
        path = config_to_xfaillist_path(config)
        if path.exists():
            with open(str(path), "r", encoding="UTF-8") as f:
                _faillist.update(set(json.load(f)))


def pytest_collection_finish(session: Session) -> None:
    for item in session.items:
        if isinstance(item, Function):
            id = item_to_test_id(item)
            if id in _faillist:
                item.add_marker(mark.xfail(reason="in xfail.list", strict=True))
