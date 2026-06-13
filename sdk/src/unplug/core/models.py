"""Backward-compatible import path → unplug.ml.models."""

from __future__ import annotations

from unplug.ml.models import (
    ModelProvider,
    ModelRegistry,
    ModelSpec,
    NullModelProvider,
)

__all__ = [
    "ModelProvider",
    "ModelRegistry",
    "ModelSpec",
    "NullModelProvider",
]
