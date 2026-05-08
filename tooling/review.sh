#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source .venv/bin/activate
ruff check .
semgrep --config p/python --error --quiet .
bandit -q -c pyproject.toml -r . -x ./.venv
pytest
echo "review OK"
