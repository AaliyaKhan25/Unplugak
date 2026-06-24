"""Tests for unplug.api.results.refresh_scan_result."""

from __future__ import annotations

from unplug.api.enums import Action
from unplug.api.results import refresh_scan_result
from unplug.api.types import Finding, ScanResult
from unplug.config.policy import ScanPolicy


def _baseline() -> ScanResult:
    return ScanResult(
        safe=True,
        action=Action.ALLOW,
        risk_score=0.0,
        findings=[],
        redacted_text="clean text",
        latency_ms=3.5,
        stages_run=["regex"],
    )


def _finding(score: float, stage: str = "privacy") -> Finding:
    return Finding(
        category="leakage",
        subcategory="pii",
        stage=stage,
        span_start=0,
        span_end=4,
        score=score,
        evidence="match",
    )


def test_recomputes_risk_from_findings() -> None:
    findings = [_finding(0.4), _finding(0.99)]
    result = refresh_scan_result("text", findings, baseline=_baseline(), policy=ScanPolicy())
    assert result.risk_score == 0.99
    assert result.findings == findings
    assert result.safe is False  # a 0.99 finding is not safe under the default policy


def test_preserves_baseline_fields_and_merges_stages() -> None:
    baseline = _baseline()
    result = refresh_scan_result(
        "text", [_finding(0.6, stage="model")], baseline=baseline, policy=ScanPolicy()
    )
    assert result.redacted_text == baseline.redacted_text
    assert result.latency_ms == baseline.latency_ms
    # baseline stage kept, new stage appended, no duplicates
    assert result.stages_run == ["regex", "model"]


def test_empty_findings_is_zero_risk() -> None:
    result = refresh_scan_result("text", [], baseline=_baseline(), policy=ScanPolicy())
    assert result.risk_score == 0.0
    assert result.findings == []
