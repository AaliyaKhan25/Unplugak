"""TaintedText model and Tagger factory."""

from __future__ import annotations

import time
import uuid

from pydantic import BaseModel, Field

from unplug.core.taint.levels import TrustLevel, trust_level_from_source
from unplug.models import Source


class TaintedText(BaseModel):
    text: str
    trust_level: TrustLevel
    origin: str
    timestamp: float = Field(default_factory=time.time)
    parent_id: str | None = None
    metadata: dict = Field(default_factory=dict)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Tagger:
    """Creates and derives TaintedText instances."""

    def tag(
        self,
        text: str,
        trust_level: TrustLevel,
        origin: str,
        *,
        parent_id: str | None = None,
        **metadata: object,
    ) -> TaintedText:
        return TaintedText(
            text=text,
            trust_level=trust_level,
            origin=origin,
            parent_id=parent_id,
            metadata=dict(metadata),
        )

    def tag_from_source(self, text: str, source: Source, origin: str) -> TaintedText:
        return self.tag(text, trust_level_from_source(source), origin)

    def derive(
        self,
        parent: TaintedText,
        new_text: str,
        **override_metadata: object,
    ) -> TaintedText:
        meta = {**parent.metadata, **override_metadata}
        return TaintedText(
            text=new_text,
            trust_level=parent.trust_level,
            origin=parent.origin,
            parent_id=parent.id,
            metadata=meta,
        )
