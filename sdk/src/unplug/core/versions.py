"""Backward-compatible import path → unplug.core.runtime.versions."""

from __future__ import annotations

import warnings

from unplug.core.runtime.versions import *  # noqa: F403

warnings.warn(
    "unplug.core.versions is deprecated; import from "
    "unplug.core.runtime.versions instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
