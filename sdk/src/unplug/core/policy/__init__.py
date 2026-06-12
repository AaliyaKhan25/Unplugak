"""Policy subpackage — decision, disposition, sensitive context."""

from __future__ import annotations

from unplug.core.policy.policy import (
    decide_action,
    flagged_coverage,
    merge_spans,
    policy_from_request,
)

__all__ = [
    "decide_action",
    "flagged_coverage",
    "merge_spans",
    "policy_from_request",
]
