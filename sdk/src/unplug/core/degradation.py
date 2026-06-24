"""Backward-compatible import path → unplug.core.agent.degradation."""

from __future__ import annotations

import warnings

from unplug.core.agent.degradation import *  # noqa: F403

warnings.warn(
    "unplug.core.degradation is deprecated; import from "
    "unplug.core.agent.degradation instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
