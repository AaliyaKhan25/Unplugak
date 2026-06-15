"""Re-export loader from unplug.config (backward compatibility)."""

from __future__ import annotations

import warnings

from unplug.config.loader import (
    _coerce,
    _merge,
    build_config,
    load,
    load_from_env,
    load_from_file,
)

__all__ = [
    "_coerce",
    "_merge",
    "build_config",
    "load",
    "load_from_env",
    "load_from_file",
]

warnings.warn(
    "unplug.core.config_loader is deprecated; import from "
    "unplug.config.loader instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
