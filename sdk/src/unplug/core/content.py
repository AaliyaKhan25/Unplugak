"""Re-export content protocol from providers (backward compatibility)."""

from __future__ import annotations

import warnings

from unplug.providers.content.protocol import CleanResult, ContentProvider, ScrapedContent

__all__ = ["CleanResult", "ContentProvider", "ScrapedContent"]

warnings.warn(
    "unplug.core.content is deprecated; import from "
    "unplug.providers.content.protocol instead (see MIGRATION.md)",
    DeprecationWarning,
    stacklevel=2,
)
