"""Backward-compatible import path → unplug.core.policy.disposition."""

from __future__ import annotations

import warnings

from unplug.core.policy.disposition import *  # noqa: F403

warnings.warn(
    "unplug.core.disposition is deprecated; import from "
    "unplug.core.policy.disposition instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
