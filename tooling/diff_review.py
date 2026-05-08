"""Локальный Reviewer: git diff → guard → Ollama (LiteLLM). Без облака по умолчанию."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess  # nosec B404
import sys
from pathlib import Path

from litellm import completion

from guard import safe_snippet

TOOLING = Path(__file__).resolve().parent
LOG_PATH = TOOLING / "logs" / "last_diff_review.txt"
DEFAULT_MAX = 28_000

# Символы, недопустимые в аргументе `git diff` (защита от подстановки команд).
_INVALID_REV_CHARS = frozenset({";", "|", "&", "$", "`", "\n", "\r", "<", ">", "(", ")"})


def _git_executable() -> str:
    exe = shutil.which("git")
    if not exe:
        raise RuntimeError("исполняемый файл git не найден в PATH")
    return exe


def _validate_revision(s: str | None) -> None:
    if s is None:
        return
    if len(s) > 300:
        raise ValueError("слишком длинный аргумент revision")
    if any(c in _INVALID_REV_CHARS for c in s):
        raise ValueError("недопустимые символы в revision (используйте ref вроде main...HEAD)")


def _git_toplevel(git_exe: str) -> Path:
    r = subprocess.run(  # nosec B603
        [git_exe, "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if r.returncode != 0:
        msg = (r.stderr or r.stdout or "").strip() or "not a git repository"
        raise RuntimeError(f"git rev-parse failed: {msg}")
    return Path(r.stdout.strip())


def get_diff_text(revision_range: str | None) -> str:
    _validate_revision(revision_range)
    git_exe = _git_executable()
    root = _git_toplevel(git_exe)
    cmd: list[str] = [git_exe, "-C", str(root), "diff"]
    if revision_range:
        cmd.append(revision_range)
    else:
        cmd.append("HEAD")
    r = subprocess.run(  # nosec B603
        cmd,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr or "")
        raise RuntimeError(f"git diff failed with exit {r.returncode}")
    return r.stdout


def clip_for_llm(diff: str, max_chars: int) -> str:
    safe = safe_snippet(diff)
    if len(safe) <= max_chars:
        return safe
    tail = "\n[... diff обрезан; увеличьте FLOW_DIFF_MAX ...]"
    return safe[: max_chars - len(tail)] + tail


def run_review(user_content: str, model: str) -> str:
    r = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты ревьюер diff. По-русски, кратко: риски, тесты, безопасность. "
                    "Не больше 5 коротких пунктов через «;» или два предложения. "
                    "Без нумерации и списков с отступами."
                ),
            },
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
    )
    out = r["choices"][0]["message"]["content"]
    return re.sub(r"(?m)^\s*\d+\.\s*", "", out).strip()


def main() -> None:
    p = argparse.ArgumentParser(description="Review git diff через guard и локальную LLM.")
    p.add_argument(
        "revision",
        nargs="?",
        default=None,
        help="Диапазон для git diff, например main...HEAD (по умолчанию: все незакоммиченные к HEAD)",
    )
    args = p.parse_args()

    max_chars = int(os.environ.get("FLOW_DIFF_MAX", str(DEFAULT_MAX)))
    model = os.environ.get("LITELLM_MODEL", "ollama/qwen2.5:0.5b")

    try:
        diff = get_diff_text(args.revision)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(2)

    if not diff.strip():
        print("Нет изменений в diff — нечего ревьюить.")
        sys.exit(0)

    try:
        payload = clip_for_llm(diff, max_chars)
    except ValueError as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(3)

    user_msg = "Изменения (patch):\n" + payload
    out = run_review(user_msg, model)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
