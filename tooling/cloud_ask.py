"""Запрос к LLM через LiteLLM после guard. По умолчанию локальный Ollama (без облачных провайдеров)."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from litellm import completion

from guard import safe_snippet

TOOLING = Path(__file__).resolve().parent
LOG_PATH = TOOLING / "logs" / "last_llm_ask.txt"
DEFAULT_MAX = 28_000
DEFAULT_MODEL = "ollama/qwen2.5:0.5b"


def _read_input(source: Path | None) -> str:
    if source is not None:
        return source.read_text(encoding="utf-8")
    return sys.stdin.read()


def prepare_payload(raw: str, max_chars: int) -> str:
    safe = safe_snippet(raw)
    if len(safe) <= max_chars:
        return safe
    tail = "\n[... текст обрезан; увеличьте FLOW_LLM_MAX или FLOW_CLOUD_MAX ...]"
    return safe[: max_chars - len(tail)] + tail


def run_llm(user_content: str, model: str) -> str:
    r = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Отвечай кратко по-русски. Два-три коротких предложения или один абзац. "
                    "Без нумерации и длинных списков."
                ),
            },
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
    )
    out = r["choices"][0]["message"]["content"]
    return re.sub(r"(?m)^\s*\d+\.\s*", "", out).strip()


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Отправить текст в модель (LiteLLM) после guard. "
            "По умолчанию локальный Ollama; модель: FLOW_LLM_MODEL "
            "(или устар. FLOW_CLOUD_MODEL), см. LiteLLM."
        ),
    )
    p.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Файл с текстом; если нет — читается stdin (без файла нужен поток через pipe)",
    )
    args = p.parse_args()

    if args.path is None and sys.stdin.isatty():
        p.error("Укажите путь к файлу или передайте текст в stdin через pipe.")

    max_chars = int(
        os.environ.get("FLOW_LLM_MAX", os.environ.get("FLOW_CLOUD_MAX", str(DEFAULT_MAX)))
    )
    model = os.environ.get("FLOW_LLM_MODEL", os.environ.get("FLOW_CLOUD_MODEL", DEFAULT_MODEL))

    raw = _read_input(Path(args.path) if args.path else None)
    if not raw.strip():
        raise SystemExit("Пустой ввод.")

    payload = prepare_payload(raw, max_chars)
    out = run_llm(payload, model)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
