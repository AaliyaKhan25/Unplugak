"""Trust levels and source mapping."""

from __future__ import annotations

from enum import StrEnum

from unplug.models import Source


class TrustLevel(StrEnum):
    TRUSTED = "trusted"
    USER = "user"
    RETRIEVED = "retrieved"
    TOOL_OUTPUT = "tool_output"
    EXTERNAL = "external"
    UNKNOWN = "unknown"


_SOURCE_TO_TRUST: dict[Source, TrustLevel] = {
    Source.SYSTEM: TrustLevel.TRUSTED,
    Source.USER: TrustLevel.USER,
    Source.RETRIEVED: TrustLevel.RETRIEVED,
    Source.TOOL_OUTPUT: TrustLevel.TOOL_OUTPUT,
}


def trust_level_from_source(source: Source) -> TrustLevel:
    return _SOURCE_TO_TRUST.get(source, TrustLevel.UNKNOWN)
