"""Backward-compatible import path → unplug.core.agent.canary."""

from __future__ import annotations

import warnings

from unplug.core.agent.canary import *  # noqa: F403

warnings.warn(
    "unplug.core.canary is deprecated; import from "
    "unplug.core.agent.canary instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
