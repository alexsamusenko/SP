# Карта Flow

Точка входа в заметки по процессу разработки и ревью. Рекомендуемый **корень хранилища Obsidian**: папка `Flow` (см. [[Подключение Obsidian]]).

## Документы

- [[architecture-phase2]] — поток агентов, каталоги `commercial` / `personal` / `external`, локальные команды
- [[Чеклист перед merge]] — перед слиянием ветки
- [[deployer-checklist]] — выкладка вручную, без автоматики из репозитория

## Быстрые команды (копипаст)

```bash
cd /mnt/d/Flow/tooling && source .venv/bin/activate
bash flow_review.sh
```

Только статика, без LLM:

```bash
FLOW_SKIP_DIFF_REVIEW=1 bash flow_review.sh
```
