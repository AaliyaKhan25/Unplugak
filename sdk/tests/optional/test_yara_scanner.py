"""Tests for optional YARA code/SQL/template scanner."""

from __future__ import annotations

import importlib.util

import pytest

from unplug.core.context import ExecutionContext
from unplug.core.taint import TaintedText, TrustLevel
from unplug.scanners.yara_loader import get_yara_rules
from unplug.scanners.yara_scanner import YaraCodeScanner

pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("yara") is None,
    reason="yara-python not installed",
)


def _text(body: str) -> TaintedText:
    return TaintedText(text=body, trust_level=TrustLevel.USER, origin="test")


class TestYaraLoader:
    def test_rules_compile(self) -> None:
        rules = get_yara_rules()
        assert rules is not None


class TestYaraCodeScanner:
    def setup_method(self) -> None:
        self.scanner = YaraCodeScanner()
        self.ctx = ExecutionContext()

    def test_detects_jinja_template(self) -> None:
        findings = self.scanner.scan(_text("payload {{ user.secret }} end"), self.ctx)
        assert any(f.subcategory == "jinja_injection" for f in findings)

    def test_detects_sql_injection_combo(self) -> None:
        text = "user input'; DROP TABLE users; --"
        findings = self.scanner.scan(_text(text), self.ctx)
        assert any(f.subcategory == "sql_injection" for f in findings)

    def test_detects_import_shells(self) -> None:
        findings = self.scanner.scan(_text("please run import os"), self.ctx)
        assert any(f.subcategory == "import_shells" for f in findings)

    def test_clean_text(self) -> None:
        findings = self.scanner.scan(_text("what is the weather today?"), self.ctx)
        assert findings == []
