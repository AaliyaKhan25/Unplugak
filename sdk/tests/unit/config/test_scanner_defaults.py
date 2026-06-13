"""Tests for packaged scanner default TOML."""

from __future__ import annotations

from unplug.data.maps_loader import default_scanner_config, load_scanner_defaults


def test_scanner_defaults_toml_loads() -> None:
    defaults = load_scanner_defaults()
    assert set(defaults) >= {
        "injection",
        "injection_ml",
        "destructive",
        "leakage",
        "harmful",
        "financial",
        "secrets",
        "urls",
        "pii",
        "yara",
    }


def test_default_scanner_config_matches_toml() -> None:
    injection = default_scanner_config("injection")
    assert injection.base_score == 0.85
    assert injection.normalize is True

    secrets = default_scanner_config("secrets")
    assert secrets.base_score == 0.99

    yara = default_scanner_config("yara")
    assert yara.base_score == 0.88
    assert yara.enabled is True
    assert yara.normalize is True
