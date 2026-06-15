"""Backward-compatible import path → unplug.core.runtime.logging."""

from __future__ import annotations

import warnings

from unplug.core.runtime.logging import *  # noqa: F403

warnings.warn(
    "unplug.core.logging is deprecated; import from "
    "unplug.core.runtime.logging instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
