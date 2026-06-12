# Branching policy

| Branch | Purpose |
|--------|---------|
| `dev` | Integration branch. **All PRs target `dev`.** CI runs here. |
| `main` | Release branch. Updated only when shipping a new version (merge from `dev`, tag, PyPI publish). |

## Day-to-day development

1. Branch from `dev`
2. Open PR → `dev`
3. Merge after CI passes

## Releasing a new version

1. Bump `sdk/pyproject.toml` version on `dev`
2. Merge `dev` → `main`
3. Tag `vX.Y.Z` on `main`
4. Publish GitHub Release (triggers PyPI workflow)
5. Fast-forward `dev` to `main` so both stay aligned
