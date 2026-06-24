"""Backward-compatible import path → unplug.core.agent.trajectory."""

from __future__ import annotations

import warnings

from unplug.core.agent.trajectory import *  # noqa: F403

warnings.warn(
    "unplug.core.trajectory is deprecated; import from "
    "unplug.core.agent.trajectory instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
