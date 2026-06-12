"""Resolve bundled audit probe files with optional local overrides."""

from __future__ import annotations

import os
from pathlib import Path

_PKG_DATA = Path(__file__).resolve().parent / "data"


def resolve_probe_path(filename: str, workspace_root: Path) -> Path:
    """Resolution order: UNPLUG_PROBES_DIR override, bundled SDK data, workspace configs/."""
    override = os.environ.get("UNPLUG_PROBES_DIR")
    if override:
        candidate = Path(override) / filename
        if candidate.is_file():
            return candidate
    bundled = _PKG_DATA / filename
    if bundled.is_file():
        return bundled
    return workspace_root / "configs" / filename
