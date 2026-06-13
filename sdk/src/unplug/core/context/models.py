"""Session tool-call model."""

from __future__ import annotations

import time

from pydantic import BaseModel, Field

from unplug.core.taint import TaintedText


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict = Field(default_factory=dict)
    taint_sources: list[TaintedText] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)
    result: TaintedText | None = None
    approved: bool | None = None
