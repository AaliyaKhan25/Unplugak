"""Privacy Filter protocol: implementation ships with unplug-safeguard model only."""

from __future__ import annotations

import logging
from typing import Protocol

from unplug.api.types import Finding
from unplug.core.secret_patterns import PF_LABEL_MAP, privacy_heuristic_patterns

_logger = logging.getLogger("unplug.privacy")

_LEAKAGE_PATTERNS = privacy_heuristic_patterns()
_PF_LABEL_MAP = PF_LABEL_MAP


class PrivacyFilterService(Protocol):
    """Server-side stage after unplug-safeguard model is released."""

    @property
    def is_loaded(self) -> bool: ...

    def scan(self, text: str, *, baseline: list[Finding]) -> list[Finding]: ...


class NullPrivacyFilter:
    """Default for SDK and server until unplug-safeguard is deployed."""

    @property
    def is_loaded(self) -> bool:
        return False

    def scan(self, text: str, *, baseline: list[Finding]) -> list[Finding]:
        return baseline


class HeuristicPrivacyFilter:
    """Regex stand-in until unplug-safeguard PF model ships."""

    @property
    def is_loaded(self) -> bool:
        return True

    def scan(self, text: str, *, baseline: list[Finding]) -> list[Finding]:
        covered = {(f.span_start, f.span_end) for f in baseline}
        extra: list[Finding] = []
        for subcategory, pattern in _LEAKAGE_PATTERNS:
            pf_label = _PF_LABEL_MAP.get(subcategory, "private_other")
            for match in pattern.finditer(text):
                span = (match.start(), match.end())
                if span in covered:
                    continue
                extra.append(
                    Finding(
                        category="leakage",
                        subcategory=pf_label,
                        stage="privacy_filter",
                        span_start=match.start(),
                        span_end=match.end(),
                        score=0.82,
                        evidence=f"Privacy filter matched {pf_label}",
                        replacement=None,
                    )
                )
                covered.add(span)
        return [*baseline, *extra]


def build_privacy_filter(
    *,
    enabled: bool,
    dev_heuristic: bool = False,
    model_source: str | None = None,
    threshold: float = 0.5,
    max_length: int = 512,
    device: str | None = None,
    local_files_only: bool = False,
    eager_load: bool = True,
) -> PrivacyFilterService:
    """Build privacy filter stage for server or SDK."""
    if not enabled:
        return NullPrivacyFilter()
    if model_source:
        from unplug.core.privacy.model_filter import TokenPrivacyFilter

        return TokenPrivacyFilter(
            model_source,
            threshold=threshold,
            max_length=max_length,
            device=device,
            local_files_only=local_files_only,
            eager_load=eager_load,
        )
    if dev_heuristic:
        return HeuristicPrivacyFilter()
    _logger.warning(
        "privacy_filter_enabled without model_source or dev_heuristic; using NullPrivacyFilter"
    )
    return NullPrivacyFilter()
