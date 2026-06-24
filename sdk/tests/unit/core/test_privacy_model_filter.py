"""Unit tests for NER privacy span decoding and filter wiring."""

from __future__ import annotations

from unplug.api.types import Finding
from unplug.core.privacy.ner_decode import decode_ner_spans, normalize_ner_label
from unplug.core.privacy.privacy import NullPrivacyFilter, build_privacy_filter


class TestNormalizeNerLabel:
    def test_bio_prefix_stripped(self) -> None:
        assert normalize_ner_label("B-EMAIL") == "EMAIL"
        assert normalize_ner_label("I-PHONE") == "PHONE"

    def test_outside_label(self) -> None:
        assert normalize_ner_label("O") == "O"


class TestDecodeNerSpans:
    def test_merges_bio_email_span(self) -> None:
        offsets = [(0, 0), (0, 5), (5, 12), (12, 12)]
        labels = ["O", "B-EMAIL", "I-EMAIL", "O"]
        scores = [0.0, 0.95, 0.93, 0.0]
        spans = decode_ner_spans(offsets, labels=labels, scores=scores, threshold=0.5)
        assert len(spans) == 1
        assert spans[0].start == 0
        assert spans[0].end == 12
        assert spans[0].entity == "EMAIL"

    def test_threshold_filters_low_confidence(self) -> None:
        offsets = [(0, 4)]
        labels = ["B-EMAIL"]
        scores = [0.2]
        spans = decode_ner_spans(offsets, labels=labels, scores=scores, threshold=0.5)
        assert spans == []


class TestBuildPrivacyFilter:
    def test_disabled_returns_null(self) -> None:
        pf = build_privacy_filter(enabled=False)
        assert isinstance(pf, NullPrivacyFilter)

    def test_dev_heuristic_loaded(self) -> None:
        pf = build_privacy_filter(enabled=True, dev_heuristic=True)
        assert pf.is_loaded is True

    def test_enabled_without_model_returns_null(self) -> None:
        pf = build_privacy_filter(enabled=True)
        assert isinstance(pf, NullPrivacyFilter)
        assert pf.is_loaded is False

    def test_scan_preserves_baseline_when_null(self) -> None:
        pf = build_privacy_filter(enabled=False)
        baseline = [
            Finding(
                category="leakage",
                subcategory="private_email",
                stage="regex",
                span_start=0,
                span_end=5,
                score=0.9,
                evidence="regex",
            )
        ]
        out = pf.scan("hello", baseline=baseline)
        assert out == baseline
