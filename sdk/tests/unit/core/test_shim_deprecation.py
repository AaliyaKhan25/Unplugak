"""Flat ``unplug.core.*`` shims must keep re-exporting and emit a DeprecationWarning."""

from __future__ import annotations

import importlib

import pytest


@pytest.mark.parametrize(
    ("module", "attr"),
    [
        ("unplug.core.cache", "ScanCache"),
        ("unplug.core.boundaries", "wrap_external_content"),
        ("unplug.core.limits", "LimitConfig"),
        ("unplug.core.config", "PipelineConfig"),
        ("unplug.core.encodings", "HeuristicEncodingClassifier"),
    ],
)
def test_flat_core_shim_warns_and_reexports(module: str, attr: str) -> None:
    mod = importlib.import_module(module)
    with pytest.warns(DeprecationWarning, match="deprecated"):
        importlib.reload(mod)
    assert hasattr(mod, attr), f"{module} must still re-export {attr}"
