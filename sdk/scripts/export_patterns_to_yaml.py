"""One-shot export of hardcoded Python patterns to YAML/TOML under src/unplug/data/."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "src" / "unplug"
DATA = ROOT / "data"


def _export_regex_list(
    patterns: list[tuple[str, re.Pattern[str]]],
    path: Path,
    *,
    default_score: float | None = None,
) -> None:
    entries: list[dict[str, object]] = []
    for name, compiled in patterns:
        entry: dict[str, object] = {"name": name, "regex": compiled.pattern}
        if compiled.flags & re.IGNORECASE:
            entry["flags"] = "i"
        if default_score is not None:
            entry["score"] = default_score
        entries.append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(entries, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> None:
    from unplug.core.pattern_loader import (
        injection_patterns,
        load_compiled_patterns,
        load_presidio_entity_map,
        secret_only_patterns,
    )
    from unplug.core.secret_patterns import PF_LABEL_MAP
    from unplug.scanners.destructive import _PATTERNS as DESTRUCTIVE
    from unplug.scanners.financial import _CRYPTO_PATTERNS, _PAYMENT_PATTERNS
    from unplug.scanners.harmful import _PATTERNS as HARMFUL
    from unplug.scanners.urls import _PATTERNS as URL_PATTERNS

    _export_regex_list(secret_only_patterns(), DATA / "patterns" / "secrets.yaml")
    _export_regex_list(
        list(load_compiled_patterns("pii_regex.yaml")),
        DATA / "patterns" / "pii_regex.yaml",
    )
    _export_regex_list(
        list(load_compiled_patterns("prompt_leak.yaml")),
        DATA / "patterns" / "prompt_leak.yaml",
    )
    _export_regex_list(injection_patterns(), DATA / "patterns" / "injection.yaml")
    _export_regex_list(DESTRUCTIVE, DATA / "patterns" / "destructive.yaml")
    _export_regex_list(HARMFUL, DATA / "patterns" / "harmful.yaml")
    _export_regex_list(_CRYPTO_PATTERNS, DATA / "patterns" / "financial_crypto.yaml")
    _export_regex_list(_PAYMENT_PATTERNS, DATA / "patterns" / "financial_payment.yaml")
    _export_regex_list(URL_PATTERNS, DATA / "patterns" / "urls.yaml")

    presidio_path = DATA / "maps" / "presidio_entities.toml"
    presidio_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for entity, (subcategory, base_score) in load_presidio_entity_map().items():
        lines.append(f"[{entity}]")
        lines.append(f'subcategory = "{subcategory}"')
        lines.append(f"base_score = {base_score}")
        lines.append("")
    presidio_path.write_text("\n".join(lines), encoding="utf-8")

    labels_path = DATA / "maps" / "privacy_labels.toml"
    label_lines = [f'"{key}" = "{label}"' for key, label in PF_LABEL_MAP.items()]
    labels_path.write_text("[labels]\n" + "\n".join(label_lines) + "\n", encoding="utf-8")

    catalog_src = ROOT / "models" / "catalog.toml"
    if catalog_src.is_file():
        text = catalog_src.read_text(encoding="utf-8")
        (DATA / "catalog.toml").write_text(text, encoding="utf-8")

    print(f"Exported patterns to {DATA}")


if __name__ == "__main__":
    main()
