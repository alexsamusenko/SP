SHELL := /bin/bash

RUFF ?= .venv/bin/ruff
PYTEST ?= .venv/bin/pytest

.PHONY: help sync lint test review flow-review coder-smoke scaffold

help:
	@echo "sync         — pip install -r requirements-dev.txt (нужен .venv)"
	@echo "lint         — ruff check ."
	@echo "test         — pytest"
	@echo "review       — bash review.sh (semgrep/ruff/bandit/pytest)"
	@echo "flow-review  — bash flow_review.sh (+ diff_review при Ollama)"
	@echo "coder-smoke  — smoke-тест локальной модели через guard"
	@echo "scaffold     — новый сервис из hello-service (make scaffold NAME=billing-api)"

sync:
	./.venv/bin/pip install -r requirements-dev.txt

lint:
	$(RUFF) check .

test:
	$(PYTEST)

review:
	bash ./review.sh

flow-review:
	bash ./flow_review.sh

coder-smoke:
	./.venv/bin/python coder_smoke.py

scaffold:
	@test -n "$(NAME)" || { echo 'Укажите: make scaffold NAME=my-service'; exit 1; }
	bash scaffold_commercial.sh "$(NAME)"
