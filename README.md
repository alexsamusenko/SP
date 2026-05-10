# Flow

Репозиторий-песочница процесса: код и заметки в одном дереве; секреты вне git (`.secrets/`, см. `.gitignore`).

## Структура

| Путь | Назначение |
|------|------------|
| `commercial/`, `personal/`, `external/` | Свои сервисы (пример: `commercial/hello-service/`), личное, чужие клоны — см. `external/README.md` |
| `tooling/` | Python-утилиты, guard, локальный LLM (Ollama + LiteLLM), скрипты ревью |
| `docs/` | Архитектура (`architecture-phase2.md`), Obsidian-хаб (`docs/brain/`) |
| `.github/` | CI и шаблон PR |

Подробнее: `docs/architecture-phase2.md` и карта `docs/brain/00 Карта Flow.md`.

## Новый Python-сервис под `commercial/`

Из шаблона `commercial/hello-service` (нужны WSL и bash):

```bash
cd /mnt/d/Flow/tooling
chmod +x scaffold_commercial.sh   # один раз
make scaffold NAME=billing-api
```

Или: `bash scaffold_commercial.sh billing-api`. Dependabot для новых папок добавьте вручную по образцу в `.github/dependabot.yml`.

## Быстрый старт (WSL)

```bash
cd /mnt/d/Flow/tooling
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
make review
```

Локальный LLM нужен там, где вызывается LiteLLM с `ollama/...`: поднят **Ollama** и нужная модель (например `qwen2.5:0.5b`). Дополнительно (с LLM-ревью diff): `make flow-review` или `bash flow_review.sh`.

## Связка с GitHub

При push выполняются проверки из `.github/workflows/ci.yml`.

Расшаренный **Ruff**: корневой `ruff.toml` (длина строки, целевая версия Python), подпроекты дублировать не нужно.

**Dependabot** (`.github/dependabot.yml`): еженедельно предлагает обновления для `tooling/requirements-dev.txt` и периодически — для GitHub Actions.

Хуки перед коммитом (один раз после клонирования):

```bash
pip install pre-commit
cd /mnt/d/Flow && pre-commit install
```
