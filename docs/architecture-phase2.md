# Поток: PR/ветка → Coder (изменения) → Tester (pytest/CI) → Reviewer (ruff/semgrep + LLM-комментарий опционально) → merge только если зелёно → Deployer вручную.
# LLM-облако: только после фильтра секретов; прод-секреты никогда в промпт.
# Каталоги: commercial | personal | external (чужие клоны).
#
# Локально один проход: `cd tooling && bash flow_review.sh` (или `FLOW_SKIP_DIFF_REVIEW=1` только статика;
# аргумент `main...HEAD` передаётся в diff_review).
#
# Заметки Obsidian и чеклисты: `docs/brain/` и `docs/deployer-checklist.md`.
