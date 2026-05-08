# Поток: PR/ветка → Coder (изменения) → Tester (pytest/CI) → Reviewer (ruff/semgrep + LLM-комментарий опционально) → merge только если зелёно → Deployer вручную.
# LLM-облако: только после фильтра секретов; прод-секреты никогда в промпт.
# Каталоги: commercial | personal | external (чужие клоны).
