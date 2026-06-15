.PHONY: install test test-security lint typecheck format fix check check-ci

install:
	cd sdk && uv sync --all-extras --dev

test:
	cd sdk && uv run pytest -v

test-security:
	cd sdk && uv run pytest \
		tests/security/test_adversarial.py \
		tests/security/test_false_positives.py \
		tests/unit/core/normalize/test_encodings.py \
		tests/security/test_secrets.py \
		tests/unit/pipelines/test_scan_policy.py \
		tests/security/test_security_stress.py \
		tests/security/test_sdk_coverage.py \
		tests/unit/core/agent/test_agent_hardening.py \
		tests/unit/scanners/test_financial.py \
		-v
	@if [ -f ../repos/unplug_exp/scripts/eval_sdk_security.py ]; then \
		cd ../repos/unplug_exp && uv run python scripts/eval_sdk_security.py --sdk ../../jakarta/sdk; \
	fi

lint:
	cd sdk && uv run ruff check .

typecheck:
	cd sdk && uv run mypy

format:
	cd sdk && uv run ruff format .

fix:
	cd sdk && uv run ruff check --fix . && uv run ruff format .

check:
	cd sdk && uv run ruff check . && uv run mypy && uv run ruff format --check . && uv run pytest -q

check-ci:
	cd sdk && make check-ci
