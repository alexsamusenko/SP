#!/usr/bin/env bash
# Копирует commercial/hello-service → commercial/<slug>, переименовывает пакет hello_service → <slug_as_module>.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO/commercial/hello-service"
SLUG="${1:-}"

if [[ -z "$SLUG" ]]; then
  echo "Usage: $(basename "$0") <service-slug>"
  echo "Example: $(basename "$0") billing-api  → каталог commercial/billing-api, пакет billing_api"
  exit 1
fi

if [[ ! "$SLUG" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Slug: только латиница нижний регистр, цифры и дефисы (например: billing-api, api2)."
  exit 1
fi

PKG="${SLUG//-/_}"
DST="$REPO/commercial/$SLUG"

if [[ -e "$DST" ]]; then
  echo "Уже существует: $DST"
  exit 1
fi

if [[ ! -d "$SRC" ]]; then
  echo "Нет шаблона $SRC — восстановите commercial/hello-service."
  exit 1
fi

cp -r "$SRC" "$DST"
rm -rf "$DST/.venv"
find "$DST" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

mv "$DST/hello_service" "$DST/$PKG"

while IFS= read -r -d '' f; do
  sed -i "s/hello_service/$PKG/g" "$f"
  sed -i "s/hello-service/$SLUG/g" "$f"
done < <(find "$DST" -type f \( -name '*.py' -o -name '*.md' -o -name '*.toml' -o -name '*.txt' \) -print0)

echo "Создано: $DST"
echo "Проверка:"
echo "  cd $DST && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt && pytest"
echo "CI уже обрабатывает все commercial/*/requirements-dev.txt автоматически."
echo "Dependabot: при необходимости добавьте в .github/dependabot.yml запись directory: /commercial/$SLUG"
