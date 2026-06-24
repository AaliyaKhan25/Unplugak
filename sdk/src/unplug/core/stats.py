"""Backward-compatible import path → unplug.core.runtime.stats."""

from __future__ import annotations

import warnings

from unplug.core.runtime.stats import *  # noqa: F403

warnings.warn(
    "unplug.core.stats is deprecated; import from "
    "unplug.core.runtime.stats instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
