import os
import re
from pathlib import Path

from litellm import completion

from guard import safe_snippet

# Экономия токенов: маленький контекст — только выбранные строки
# Лимит: облако не используем — только ollama локально


def main() -> None:
    root = Path("/mnt/d/Flow/personal/readme.txt")
    snippet = (
        root.read_text(encoding="utf-8")
        if root.exists()
        else "Напиши одну строку: проект Flow стартовал."
    )
    msg = safe_snippet(snippet)[:4000]
    r = completion(
        model=os.environ.get("LITELLM_MODEL", "ollama/qwen2.5:0.5b"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Отвечай кратко по-русски. Ровно два коротких предложения подряд. "
                    "Запрещены списки, нумерация и маркеры."
                ),
            },
            {"role": "user", "content": msg},
        ],
        temperature=0.2,
    )
    out = r["choices"][0]["message"]["content"]
    out = re.sub(r"(?m)^\s*\d+\.\s*", "", out).strip()
    Path("/mnt/d/Flow/tooling/logs/last_run.txt").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
