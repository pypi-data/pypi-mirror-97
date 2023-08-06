from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.python import Function


def config_to_xfaillist_path(config: Config) -> Path:
    return Path(config.rootpath, "xfails.list")


def item_to_test_id(item: Function) -> str:
    function = item.function
    return f"{function.__module__}.{item.name}"
