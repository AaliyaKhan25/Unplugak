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
        samples = {
            "anthropic_key": (
                "key sk-ant-SCRUBBED"
                "AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGh"
            ),
            "google_api_key": "AIzaSy_SCRUBBED",
            "huggingface_token": "hf_SCRUBBED",
            "gitlab_token": "glpat-SCRUBBED",
            "stripe_secret": "sk_live_SCRUBBED",
            "stripe_restricted": "rk_test_SCRUBBED",
            "npm_token": "npm_SCRUBBED",
            "sendgrid_key": "SG.SCRUBBED",
            "twilio_key": "SK_SCRUBBED",
            "bearer_token": "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
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
            text="deploy with hf_SCRUBBED",
            trust_level=TrustLevel.TOOL_OUTPUT,
            origin="test",
        )
        findings = list(scanner.scan(text, ExecutionContext()))
        subs = {f.subcategory for f in findings}
        assert "huggingface_token" in subs
