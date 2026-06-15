# Migration & deprecation guide

This documents deprecated import paths and APIs, the canonical replacement, and
when each will be removed. Deprecated paths keep working until the listed removal
version so you can migrate on your own schedule.

## API stability tiers

`import unplug` exposes three tiers. Depend freely on **Stable**; pin a version
before depending on **Provisional**; treat **Internal** as private (it can change
in any release).

| Tier | Symbols | Guarantee |
|------|---------|-----------|
| **Stable** | `Guard`, `GuardConfig`, `TaintedText`, `TrustLevel`, `Source`, `Finding`, `ScanResult`, `Action`, `ScanPolicy`, `SecretsRegistry`, `ExecutionContext`, `ToolCall`, `UnplugClient`, `load_config`, exceptions (`ConfigError`, `ServerError`) | No breaking changes within a major version |
| **Provisional** | `ModelProvider`, `ModelRegistry`, `ModelSpec`, `PipelineConfig`, `ThresholdConfig`, `MessageConfig`, `LimitConfig`, `ScannerConfig`, `MetricsCollector`, `correlation_scope`, `get_correlation_id` | May change with a minor-version note |
| **Internal** | `BaseScanner`, `ModelScanner`, `RegexScanner`, `Tagger`, `SafeguardRegistry`, anything under `unplug.core.*`, `unplug.guard_scan` | No stability guarantee — import at your own risk |

## Deprecated paths (removed in v1.0)

| Deprecated | Use instead | Notes |
|------------|-------------|-------|
| `unplug.safeguards.*` | `unplug.scanners.*` | `scanners/` is canonical; `safeguards/` is a shim |
| `SafeguardRegistry` | `ScannerRegistry` | alias kept importable from top level |
| `unplug.scanner` (module) | `unplug.scanners` | |
| Flat `unplug.core.<name>` shims (e.g. `core.canary`, `core.cache`, `core.intent`, `core.taint`, …) | their subpackage home (e.g. `core.agent.canary`, `core.runtime.cache`, `core.agent.intent`, `core.taint.*`) | ~25 modules re-export from subpackages |
| `fail_closed=false` / `fail_mode="open"` | (removed) | errors always fail closed; the flag is ignored |

## Notes / known follow-ups

- **`unplug.guard_scan.refresh_scan_result`** is currently consumed cross-repo by
  `unplug-server`. It is **Internal** today; before v1.0 it will move to a stable
  public module with a back-compat shim, coordinated with the server. Do not build
  new external dependencies on `unplug.guard_scan`.
- The flat `core.*` shims do **not** all emit a `DeprecationWarning` yet; this guide
  is the source of truth for the removal plan. Per-shim runtime warnings are a
  tracked follow-up.

## Removal timeline

- **v0.x:** deprecated paths work; this guide tracks them.
- **v1.0:** all paths in the table above are removed. Migrate before upgrading to v1.0.
