"""Backward-compatible import path → unplug.core.agent.toolchain."""

from __future__ import annotations

import warnings

from unplug.core.agent.toolchain import *  # noqa: F403

warnings.warn(
    "unplug.core.toolchain is deprecated; import from "
    "unplug.core.agent.toolchain instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
