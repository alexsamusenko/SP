# hello-service

Шаблон одного приложения под `commercial/`. Отдельное окружение (рекомендуется):

```bash
cd commercial/hello-service
python3 -m venv .venv
source .venv/bin/activate
pip install pytest ruff
ruff check .
pytest
python -m hello_service.main
```

CI в корневом репозитории также гоняет для этой папки `ruff` и `pytest`.
