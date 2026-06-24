"""Backward-compatible import path → unplug.core.privacy.luhn."""

from __future__ import annotations

import warnings

from unplug.core.privacy.luhn import *  # noqa: F403

warnings.warn(
    "unplug.core.luhn is deprecated; import from "
    "unplug.core.privacy.luhn instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
