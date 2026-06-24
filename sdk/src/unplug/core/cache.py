"""Backward-compatible import path → unplug.core.runtime.cache."""

from __future__ import annotations

import warnings

from unplug.core.runtime.cache import *  # noqa: F403

warnings.warn(
    "unplug.core.cache is deprecated; import from "
    "unplug.core.runtime.cache instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
