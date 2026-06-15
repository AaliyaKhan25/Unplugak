"""Backward-compatible import path → unplug.core.agent.intent."""

from __future__ import annotations

import warnings

from unplug.core.agent.intent import *  # noqa: F403

warnings.warn(
    "unplug.core.intent is deprecated; import from "
    "unplug.core.agent.intent instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
