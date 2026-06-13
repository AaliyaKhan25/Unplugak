# Contributing to Unplug

**Unplug the bad AI.**

## Getting started (fork workflow)

1. Fork [UnplugAI/Unplug](https://github.com/UnplugAI/Unplug) and clone your fork.
2. Set up the SDK:

```bash
cd sdk
uv sync --all-extras --dev   # everything, including optional extras
# or minimal core only:
uv sync --dev
```

3. Optional extras map to scanner features — install only what you touch:

| Extra | Enables |
|-------|---------|
| `ml` | ML span model (`Guard.with_tiny()`) |
| `yara` | YARA code/SQLi/XSS scanner |
| `presidio` | Presidio PII scanner |
| `litellm` | LLM judge for borderline cases |
| `haystack` | Haystack RAG integration |
| `scrape` | Firecrawl content provider |

4. Verify your environment: `make check` (lint + format + tests).

## Branching and PRs

- Do **not** push directly to `main`.
- Branch from **`dev`**: `feature/<short-name>` or `fix/<short-name>`.
- Open a PR targeting **`dev`**; iterate in review until green CI.
- Merge via squash or merge commit after approval.
- `main` is release-only — see [`.github/BRANCHING.md`](.github/BRANCHING.md).
- Releases are tagged from `main` and published by maintainers — see [`sdk/PUBLISH.md`](sdk/PUBLISH.md).

## What not to commit

- Internal strategy, competitive analysis, or business planning docs
- Agent session transcripts or private `.context/` material
- Secrets (`.env`, API keys, credentials)

Keep internal notes local or in a private repository.

## CI

GitHub Actions runs on every PR to `dev` ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

1. **Ruff** — `ruff check .` + `ruff format --check .`
2. **Tests** — full pytest suite (`pytest -q`)
3. **Exfil demo gate** — `test_exfil_demo_integration.py` + `sdk/examples/agent_exfil_demo.py`
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

## Test layout

`sdk/tests/` mirrors `sdk/src/unplug/`:

```bash
uv run pytest tests/unit           # fast, no optional deps
uv run pytest tests/unit/core      # core subpackages (taint, normalize, policy, ...)
uv run pytest tests/integration    # Guard end-to-end, client, examples
uv run pytest tests/security       # adversarial + regression gate
uv run pytest tests/optional       # presidio / yara / haystack / litellm (skip when extras missing)
```

Every new module gets a test file in the mirrored location.

ML checkpoint tests skip unless `UNPLUG_TEST_CHECKPOINT` (or `UNPLUG_MODEL_PATH`)
points at a local checkpoint directory — see `.env.example`.

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
