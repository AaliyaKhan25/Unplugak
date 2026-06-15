"""Backward-compatible import path → unplug.core.privacy.secrets."""

from __future__ import annotations

import warnings

from unplug.core.privacy.secrets import *  # noqa: F403

warnings.warn(
    "unplug.core.secrets is deprecated; import from "
    "unplug.core.privacy.secrets instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
