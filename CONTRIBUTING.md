# Contributing to Unplug

**Unplug the bad AI.**

## Branching and PRs

- Do **not** push directly to `main`.
- Branch from **`dev`**: `feature/<short-name>` or `fix/<short-name>`.
- Open a PR targeting **`dev`**; iterate in review until green CI.
- Merge via squash or merge commit after approval.
- `main` is release-only — see [`.github/BRANCHING.md`](.github/BRANCHING.md).

## What not to commit

- Internal strategy, competitive analysis, or business planning docs
- Agent session transcripts or private `.context/` material
- Secrets (`.env`, API keys, credentials)

Keep internal notes local or in a private repository.

## CI

GitHub Actions runs on every PR to `dev` ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

1. **Ruff** — `ruff check .` + `ruff format --check .`
2. **Tests** — full pytest suite (`pytest -q`)
3. **Exfil demo gate** — `test_exfil_demo_integration.py` + `examples/agent_exfil_demo.py`
4. **Security regression** — explicit subset (adversarial, encodings, secrets, agent hardening, etc.)

## Local checks (SDK)

```bash
cd sdk
uv sync --all-extras --dev

# Fast local gate (lint + format + full pytest)
make check

# Exact CI parity before PR (includes exfil demo + security subset)
make check-ci

# Auto-fix formatting and safe lint fixes
make fix

# Individual targets
make lint
make format
make test
make test-security
make audit
make audit-ml
```

From repo root: `make check`, `make check-ci`, `make fix`, `make test`.

## Code conventions

- Python 3.11+, `uv`, ruff, pytest
- `from __future__ import annotations` in every file
- Type all function parameters and return values
- Pydantic `BaseModel` for data models
- Architecture layering: Guard → Pipelines → Scanners → Core
- Fail closed: scanner/pipeline errors → block, never allow silently
- Import scanners from **`unplug.scanners.*`** (canonical namespace)

## Agent integration

When adding scanner or pipeline behavior, read the **agent host checklist** in [`sdk/README.md`](sdk/README.md) and run `unplug-audit` (plus `--probes` when touching detection).

## Related repos

| Repo | Role |
|------|------|
| [Unplug](https://github.com/UnplugAI/Unplug) | SDK (this repo) |
| [unplug-server](https://github.com/UnplugAI/unplug-server) | Hosted API |
| [unplug-mcp](https://github.com/UnplugAI/unplug-mcp) | MCP tools |

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
