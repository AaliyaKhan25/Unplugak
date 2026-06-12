"""Compile bundled YARA rules (requires yara-python extra)."""

from __future__ import annotations

import threading
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from unplug.optional.yara import get_yara_module

_RULE_NAMES = ("code", "sqli", "template", "xss")

_lock = threading.Lock()
_rules: Any | None = None
_load_error: str | None = None


@lru_cache(maxsize=1)
def _rules_dir() -> Path:
    return Path(resources.files("unplug.data")).joinpath("yara_rules")


def get_yara_rules() -> Any:
    """Return compiled YARA rules. Raises if rules fail to compile."""
    global _rules, _load_error

    if _rules is not None:
        return _rules
    if _load_error is not None:
        raise RuntimeError(_load_error)

    with _lock:
        if _rules is not None:
            return _rules
        if _load_error is not None:
            raise RuntimeError(_load_error)

        rules_dir = _rules_dir()
        filepaths = {
            name: str(rules_dir / f"{name}.yara")
            for name in _RULE_NAMES
            if (rules_dir / f"{name}.yara").is_file()
        }
        if not filepaths:
            _load_error = f"no bundled YARA rules under {rules_dir}"
            raise RuntimeError(_load_error)

        try:
            yara = get_yara_module()
            _rules = yara.compile(filepaths=filepaths)
        except Exception as exc:
            _load_error = f"YARA compile failed: {type(exc).__name__}: {exc}"
            raise RuntimeError(_load_error) from exc

        return _rules
