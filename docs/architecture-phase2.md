# Поток: PR/ветка → Coder (изменения) → Tester (pytest/CI) → Reviewer (ruff/semgrep + LLM-комментарий опционально) → merge только если зелёно → Deployer вручную.
# Внешние LLM (опционально): только после фильтра секретов; прод-секреты никогда в промпт.
# Каталоги: commercial | personal | external (чужие клоны; см. external/README.md).
#
# Локально один проход: `cd tooling && bash flow_review.sh` (или `FLOW_SKIP_DIFF_REVIEW=1` только статика;
# аргумент `main...HEAD` передаётся в diff_review).
#
# Заметки Obsidian и чеклисты: `docs/brain/` и `docs/deployer-checklist.md`.
# Коротко о репозитории: см. `README.md` в корне; команды — `tooling/Makefile` (`make review`).
# Зависимости tooling: предложения обновлений через Dependabot (`.github/dependabot.yml`).
# Новый сервис: `tooling/scaffold_commercial.sh <slug>` от `commercial/hello-service`; CI гоняет все `commercial/*/requirements-dev.txt`.
#
# Доп. LLM (вручную): `tooling/cloud_ask.py` — по умолчанию локальный Ollama; модель `FLOW_LLM_MODEL`.
# Перед отправкой текст через `guard`. Образец переменных: `tooling/env.llm.example`.
