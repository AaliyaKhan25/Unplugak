"""Load and compile packaged YAML/TOML pattern assets."""

from __future__ import annotations

import re
import tomllib
from functools import lru_cache
from importlib import resources
from typing import Literal

import yaml

from unplug.core.schemas.patterns import EntityMapEntry, LabelMap, PatternEntry

_FLAG_MAP: dict[str, int] = {"i": re.IGNORECASE}


def _compile_flags(flags: str | None) -> int:
    if not flags:
        return 0
    combined = 0
    for char in flags:
        if char not in _FLAG_MAP:
            msg = f"unsupported regex flag: {char!r}"
            raise ValueError(msg)
        combined |= _FLAG_MAP[char]
    return combined


def _compile_pattern(entry: PatternEntry) -> re.Pattern[str]:
    try:
        return re.compile(entry.regex, _compile_flags(entry.flags))
    except re.error as exc:
        msg = f"invalid regex for pattern {entry.name!r}: {exc}"
        raise ValueError(msg) from exc


def _read_text(package: str, resource: str) -> str:
    return resources.files(package).joinpath(resource).read_text(encoding="utf-8")


@lru_cache(maxsize=32)
def load_pattern_entries(resource: str) -> tuple[PatternEntry, ...]:
    raw = _read_text("unplug.data.patterns", resource)
    data = yaml.safe_load(raw)
    if not isinstance(data, list):
        msg = f"{resource}: expected YAML list"
        raise TypeError(msg)
    return tuple(PatternEntry.model_validate(item) for item in data)


@lru_cache(maxsize=32)
def load_compiled_patterns(resource: str) -> tuple[tuple[str, re.Pattern[str]], ...]:
    return tuple((entry.name, _compile_pattern(entry)) for entry in load_pattern_entries(resource))


@lru_cache(maxsize=8)
def load_presidio_entity_map() -> dict[str, tuple[str, float]]:
    raw = _read_text("unplug.data.maps", "presidio_entities.toml")
    parsed = tomllib.loads(raw)
    result: dict[str, tuple[str, float]] = {}
    for entity, values in parsed.items():
        entry = EntityMapEntry.model_validate(values)
        result[entity] = (entry.subcategory, entry.base_score)
    return result


@lru_cache(maxsize=4)
def load_privacy_label_map() -> dict[str, str]:
    raw = _read_text("unplug.data.maps", "privacy_labels.toml")
    parsed = tomllib.loads(raw)
    labels = LabelMap.model_validate(parsed)
    return dict(labels.labels)


def leakage_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Secrets + PII + prompt-leak patterns for the leakage scanner."""
    combined: list[tuple[str, re.Pattern[str]]] = []
    for resource in ("secrets.yaml", "pii_regex.yaml", "prompt_leak.yaml"):
        combined.extend(load_compiled_patterns(resource))
    return combined


def secret_only_patterns() -> list[tuple[str, re.Pattern[str]]]:
    return list(load_compiled_patterns("secrets.yaml"))


def privacy_heuristic_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Subset used by the dev privacy-filter heuristic."""
    compiled = dict(load_compiled_patterns("secrets.yaml"))
    pii = dict(load_compiled_patterns("pii_regex.yaml"))
    names = ("api_key_generic", "aws_key", "email_address", "phone_number")
    result: list[tuple[str, re.Pattern[str]]] = []
    for name in names:
        pattern = compiled.get(name) or pii.get(name)
        if pattern is not None:
            result.append((name, pattern))
    return result


def injection_patterns() -> list[tuple[str, re.Pattern[str]]]:
    return list(load_compiled_patterns("injection.yaml"))


PatternResource = Literal[
    "secrets.yaml",
    "pii_regex.yaml",
    "prompt_leak.yaml",
    "injection.yaml",
    "destructive.yaml",
    "harmful.yaml",
    "financial_crypto.yaml",
    "financial_payment.yaml",
    "urls.yaml",
]
