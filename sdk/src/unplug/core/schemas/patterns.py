"""Schemas for packaged pattern/m map assets."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class PatternEntry(BaseModel):
    name: str
    regex: str
    flags: str | None = None
    score: float | None = None
    replacement: str | None = None

    @field_validator("regex")
    @classmethod
    def _non_empty_regex(cls, value: str) -> str:
        if not value.strip():
            msg = "pattern regex must not be empty"
            raise ValueError(msg)
        return value


class EntityMapEntry(BaseModel):
    subcategory: str
    base_score: float


class LabelMap(BaseModel):
    labels: dict[str, str] = Field(default_factory=dict)
