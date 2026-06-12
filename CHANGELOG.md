# Changelog

All notable changes to the `unplug-ai` SDK.

## [Unreleased]

### Changed

- **Tagline:** "Unplug the bad AI" (README, pyproject, package docstring)
- **Canonical namespace:** `unplug.scanners.*` replaces `unplug.safeguards.*`
- **Core layout:** `core/` split into subpackages (`taint/`, `normalize/`, `policy/`, `agent/`, `privacy/`, `runtime/`, `redaction/`) with flat shims until v1.0
- **Patterns externalized:** Regex lists in `data/patterns/*.yaml`; maps in `data/maps/*.toml`; loaded via `core/pattern_loader.py`
- **Optional deps:** Fail-loud `unplug.optional.*` modules replace `is_available()` soft skips
- **YARA rules:** Bundled under `data/yara_rules/`

### Deprecated

- `unplug.safeguards` — import from `unplug.scanners` (removed v1.0)
- `SafeguardRegistry` — use `ScannerRegistry` (removed v1.0)
- Flat `unplug.core.*` shim modules — import from subpackages (removed v1.0)

### Added

- `CODE_OF_CONDUCT.md`, `SECURITY.md` at repo root
- `sdk/docs/ARCHITECTURE.md`, `RESTRUCTURE_PLAN.md`, `LOGIC_AUDIT.md`
- Runtime dependency: `pyyaml`
- `tests/unit/core/test_pattern_loader.py`

## [0.3.0] — 2026-06-01

- Dev branch workflow; PyPI publish from `main`
- Safeguard registry, ML span model preview, agent hardening suite
