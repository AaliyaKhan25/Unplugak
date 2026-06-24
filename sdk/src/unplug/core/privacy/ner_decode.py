"""Decode token-classification NER tags into character spans."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NerCharSpan:
    start: int
    end: int
    entity: str
    score: float


def normalize_ner_label(label: str) -> str:
    """Strip BIO/BIOES prefix and return uppercase entity name or O."""
    tag = label.strip().upper()
    if tag in {"O", "OUTSIDE", "OTHER"}:
        return "O"
    if "-" in tag:
        prefix, entity = tag.split("-", 1)
        if prefix in {"B", "I", "E", "S"}:
            return entity.strip().upper() or "O"
    return tag


def decode_ner_spans(
    offset_mapping: list[tuple[int, int]],
    *,
    labels: list[str],
    scores: list[float],
    threshold: float,
) -> list[NerCharSpan]:
    """Merge per-token NER predictions into character spans."""
    spans: list[NerCharSpan] = []
    current: NerCharSpan | None = None

    for (start, end), raw_label, score in zip(offset_mapping, labels, scores, strict=True):
        if start == end == 0:
            continue
        entity = normalize_ner_label(raw_label)
        conf = float(score)
        if entity == "O" or conf < threshold:
            if current is not None:
                spans.append(current)
                current = None
            continue

        prefix = raw_label.strip().upper().split("-", 1)[0] if "-" in raw_label else ""
        starts_new = prefix in {"B", "S"} or current is None or current.entity != entity

        if starts_new:
            if current is not None:
                spans.append(current)
            current = NerCharSpan(start=start, end=end, entity=entity, score=conf)
        elif current is not None:
            current = NerCharSpan(
                start=current.start,
                end=end,
                entity=entity,
                score=max(current.score, conf),
            )
        else:
            current = NerCharSpan(start=start, end=end, entity=entity, score=conf)

        if prefix in {"E", "S"} and current is not None:
            spans.append(current)
            current = None

    if current is not None:
        spans.append(current)
    return spans
