"""Backward-compatible import path → unplug.core.normalize.encodings."""

from __future__ import annotations

import warnings

from unplug.core.normalize.encodings import *  # noqa: F403

warnings.warn(
    "unplug.core.encodings is deprecated; import from "
    "unplug.core.normalize.encodings instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
