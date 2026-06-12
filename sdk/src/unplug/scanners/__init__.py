"""Canonical scanner registry and base types."""

from __future__ import annotations

from unplug.scanners.base import BaseScanner, ModelScanner, RegexScanner, Scanner
from unplug.scanners.registry import ScannerRegistry

__all__ = [
    "BaseScanner",
    "ModelScanner",
    "RegexScanner",
    "SafeguardRegistry",
    "Scanner",
    "ScannerRegistry",
]


def __getattr__(name: str) -> type[ScannerRegistry]:
    # Lazy so the DeprecationWarning fires on use, not on package import.
    if name == "SafeguardRegistry":
        from unplug.scanners import registry

        return registry.SafeguardRegistry
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
