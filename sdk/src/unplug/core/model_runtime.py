"""Backward-compatible import path → unplug.core.runtime.model_runtime."""

from __future__ import annotations

import warnings

from unplug.core.runtime.model_runtime import *  # noqa: F403

warnings.warn(
    "unplug.core.model_runtime is deprecated; import from "
    "unplug.core.runtime.model_runtime instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
