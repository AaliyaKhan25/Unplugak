"""Tests for shared secret-token and leakage regex patterns."""

from __future__ import annotations

from unplug.core.context import ExecutionContext
from unplug.core.pattern_loader import load_compiled_patterns
from unplug.core.secret_patterns import leakage_patterns, secret_only_patterns
from unplug.core.taint import TaintedText, TrustLevel
from unplug.scanners.leakage import LeakageScanner


def _match(subcategory: str, text: str) -> bool:
    patterns = dict(leakage_patterns())
    return patterns[subcategory].search(text) is not None


class TestSecretTokenPatterns:
    def test_expanded_provider_tokens(self) -> None:
        # Fixture tokens are assembled from parts so no literal in this file
        # is token-shaped (keeps GitHub push protection and similar secret
        # scanners from flagging the test suite itself).
        samples = {
            "anthropic_key": (
                "key sk-ant-" + "api03-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
                "AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGh"
            ),
            "google_api_key": "AIzaSy" + "Dtest1234567890123456789012345678",
            "huggingface_token": "hf_" + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJ",
            "gitlab_token": "glpat-" + "abcdefghijklmnopqrst",
            "stripe_secret": "sk_live_" + "abcdefghijklmnopqrstuvwx",
            "stripe_restricted": "rk_test_" + "abcdefghijklmnopqrstuvwx",
            "npm_token": "npm_" + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJ",
            "sendgrid_key": "SG." + "abcdefghijklmnopqrstuv.wxyz1234567890abcdefghijklmnop",
            "twilio_key": "SK" + "0123456789abcdef0123456789abcdef",
            "bearer_token": "Authorization: Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        }
        for subcategory, text in samples.items():
            assert _match(subcategory, text), subcategory

    def test_secret_only_is_subset_of_leakage(self) -> None:
        secret_names = {name for name, _ in secret_only_patterns()}
        leakage_secret_names = {name for name, _ in load_compiled_patterns("secrets.yaml")}
        assert secret_names == leakage_secret_names

    def test_leakage_scanner_detects_new_tokens(self) -> None:
        scanner = LeakageScanner()
        text = TaintedText(
            text="deploy with hf_" + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJ",
            trust_level=TrustLevel.TOOL_OUTPUT,
            origin="test",
        )
        findings = list(scanner.scan(text, ExecutionContext()))
        subs = {f.subcategory for f in findings}
        assert "huggingface_token" in subs
