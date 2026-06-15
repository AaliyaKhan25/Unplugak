"""Re-export limits from unplug.config (backward compatibility)."""

from __future__ import annotations

import warnings

from unplug.config.limits import LimitConfig, LimitViolation, estimate_tokens

__all__ = ["LimitConfig", "LimitViolation", "estimate_tokens"]

warnings.warn(
    "unplug.core.limits is deprecated; import from unplug.config.limits instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
