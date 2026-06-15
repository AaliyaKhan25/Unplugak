"""Backward-compatible import path → unplug.core.agent.boundaries."""

from __future__ import annotations

import warnings

from unplug.core.agent.boundaries import *  # noqa: F403

warnings.warn(
    "unplug.core.boundaries is deprecated; import from "
    "unplug.core.agent.boundaries instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
