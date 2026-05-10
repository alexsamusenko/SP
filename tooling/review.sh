#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source .venv/bin/activate
ruff check .
# Исключаем .venv (в CI его нет; локально иначе Semgrep лезет в site-packages).
semgrep --config p/python --error --quiet \
  --exclude '.venv' \
  --exclude '.pytest_cache' \
  .
bandit -q -c pyproject.toml -r . -x ./.venv
pytest
echo "review OK"
