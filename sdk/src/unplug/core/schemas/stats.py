"""Pydantic models for scanner and pipeline metrics."""

from __future__ import annotations

from pydantic import BaseModel


class ScannerStats(BaseModel):
    """Per-scanner statistics."""

    scans: int = 0
    findings: int = 0
    total_latency_ms: float = 0.0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.scans if self.scans else 0.0

    @property
    def hit_rate(self) -> float:
        return self.findings / self.scans if self.scans else 0.0

    def to_dict(self) -> dict:
        return {
            "scans": self.scans,
            "findings": self.findings,
            "avg_latency_ms": round(self.avg_latency_ms, 3),
            "hit_rate": round(self.hit_rate, 4),
        }


class PipelineStats(BaseModel):
    """Per-pipeline statistics."""

    runs: int = 0
    total_latency_ms: float = 0.0
    blocked: int = 0
    redacted: int = 0
    reviewed: int = 0
    allowed: int = 0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.runs if self.runs else 0.0

    def to_dict(self) -> dict:
        return {
            "runs": self.runs,
            "avg_latency_ms": round(self.avg_latency_ms, 3),
            "blocked": self.blocked,
            "redacted": self.redacted,
            "reviewed": self.reviewed,
            "allowed": self.allowed,
        }
