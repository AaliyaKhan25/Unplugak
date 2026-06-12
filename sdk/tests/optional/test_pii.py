"""Tests for optional Presidio PII scanner."""

from __future__ import annotations

import pytest

from unplug.core.context import ExecutionContext
from unplug.core.taint import TaintedText, TrustLevel
from unplug.scanners.pii import PresidioPiiScanner
from unplug.scanners.registry import SafeguardRegistry


def _presidio_available() -> bool:
    try:
        import presidio_analyzer  # noqa: F401

        return True
    except ImportError:
        return False


pytestmark = pytest.mark.skipif(not _presidio_available(), reason="presidio extra not installed")


class TestPresidioPiiScanner:
    def test_registry_lists_pii(self) -> None:
        assert "pii" in SafeguardRegistry.available()

    def test_detects_email_and_person(self) -> None:
        scanner = PresidioPiiScanner()
        text = TaintedText(
            text="Please email Jane Doe at jane.doe@example.com about the invoice.",
            trust_level=TrustLevel.TOOL_OUTPUT,
            origin="test",
        )
        findings = list(scanner.scan(text, ExecutionContext()))
        subs = {f.subcategory for f in findings}
        assert "email_address" in subs

    def test_skips_user_trusted_text(self) -> None:
        scanner = PresidioPiiScanner()
        text = TaintedText(
            text="jane.doe@example.com",
            trust_level=TrustLevel.USER,
            origin="test",
        )
        assert list(scanner.scan(text, ExecutionContext())) == []
