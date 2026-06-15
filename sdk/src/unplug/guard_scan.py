"""Deprecated module path. Use ``unplug.api.results`` instead.

Kept as a back-compat shim; will be removed in v1.0 (see MIGRATION.md).
"""

from __future__ import annotations

import warnings

from unplug.api.results import refresh_scan_result

warnings.warn(
    "unplug.guard_scan is deprecated; import refresh_scan_result from unplug.api.results",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["refresh_scan_result"]
