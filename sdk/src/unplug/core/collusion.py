"""Backward-compatible import path → unplug.core.agent.collusion."""

from __future__ import annotations

import warnings

from unplug.core.agent.collusion import *  # noqa: F403

warnings.warn(
    "unplug.core.collusion is deprecated; import from "
    "unplug.core.agent.collusion instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
