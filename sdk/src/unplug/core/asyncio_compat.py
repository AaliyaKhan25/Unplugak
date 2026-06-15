"""Backward-compatible import path → unplug.core.runtime.asyncio_compat."""

from __future__ import annotations

import warnings

from unplug.core.runtime.asyncio_compat import *  # noqa: F403

warnings.warn(
    "unplug.core.asyncio_compat is deprecated; import from "
    "unplug.core.runtime.asyncio_compat instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
