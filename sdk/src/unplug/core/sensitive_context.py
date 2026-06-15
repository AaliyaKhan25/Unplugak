"""Backward-compatible import path → unplug.core.policy.sensitive_context."""

from __future__ import annotations

import warnings

from unplug.core.policy.sensitive_context import *  # noqa: F403

warnings.warn(
    "unplug.core.sensitive_context is deprecated; import from "
    "unplug.core.policy.sensitive_context instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
