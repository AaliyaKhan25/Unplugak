"""Backward-compatible import path → unplug.core.agent.approval."""

from __future__ import annotations

import warnings

from unplug.core.agent.approval import *  # noqa: F403

warnings.warn(
    "unplug.core.approval is deprecated; import from "
    "unplug.core.agent.approval instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
