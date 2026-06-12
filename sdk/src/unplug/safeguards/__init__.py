"""Deprecated import path — use unplug.scanners instead."""

from __future__ import annotations

import warnings

warnings.warn(
    "unplug.safeguards is deprecated; import from unplug.scanners instead",
    DeprecationWarning,
    stacklevel=2,
)

from unplug.scanners import SafeguardRegistry, ScannerRegistry
from unplug.scanners.base import BaseScanner, ModelScanner, RegexScanner, Scanner

__all__ = [
    "BaseScanner",
    "ModelScanner",
    "RegexScanner",
    "SafeguardRegistry",
    "Scanner",
    "ScannerRegistry",
]
