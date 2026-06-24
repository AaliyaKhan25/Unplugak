"""Backward-compatible import path → unplug.core.policy.decision."""

from __future__ import annotations

import warnings

from unplug.core.policy.decision import *  # noqa: F403

warnings.warn(
    "unplug.core.decision is deprecated; import from "
    "unplug.core.policy.decision instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
