# Экономия токенов: один скрипт создаёт все файлы — меньше ошибок ручного копирования
from __future__ import annotations

import textwrap
from pathlib import Path

FLOW = Path("/mnt/d/Flow")
TOOL = FLOW / "tooling"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip("\n") + "\n", encoding="utf-8")
    print("wrote", path)


def main() -> None:
    write(
        TOOL / "guard.py",
        """
        FORBIDDEN = (".env", ".pem", "id_rsa", "aws_", "BEGIN PRIVATE")


        def safe_snippet(text: str) -> str:
            lower = text.lower()
            if any(x in lower for x in FORBIDDEN):
                raise ValueError("blocked: похоже на секрет — не отправляем в LLM")
            return text
        """,
    )

    write(
        TOOL / "coder_smoke.py",
        """
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
            out = re.sub(r"(?m)^\\s*\\d+\\.\\s*", "", out).strip()
            Path("/mnt/d/Flow/tooling/logs/last_run.txt").write_text(out, encoding="utf-8")
            print(out)


        if __name__ == "__main__":
            main()
        """,
    )

    write(
        TOOL / "pyproject.toml",
        """
        [project]
        name = "flow-tooling"
        version = "0.1.0"
        requires-python = ">=3.12"

        [tool.ruff]
        line-length = 100
        target-version = "py312"

        [tool.pytest.ini_options]
        pythonpath = ["."]
        testpaths = ["tests"]
        addopts = "-q"

        [tool.bandit]
        exclude_dirs = [".venv", "tests"]
        skips = ["B101"]
        """,
    )

    write(
        TOOL / "requirements-dev.txt",
        """
        litellm>=1.83
        ruff>=0.15
        semgrep>=1.160
        pytest>=8
        bandit[toml]>=1.7
        """,
    )

    write(
        TOOL / "tests/test_guard.py",
        """
        import pytest

        from guard import safe_snippet


        def test_safe_accepts_normal_text() -> None:
            assert "hello" in safe_snippet("hello world")


        def test_safe_blocks_secrets() -> None:
            with pytest.raises(ValueError):
                safe_snippet("BEGIN PRIVATE\\n-----")
        """,
    )

    write(
        TOOL / "review.sh",
        """
        #!/usr/bin/env bash
        set -euo pipefail
        ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        cd "$ROOT"
        source .venv/bin/activate
        ruff check .
        semgrep --config p/python --error --quiet .
        bandit -q -c pyproject.toml -r . -x ./.venv
        pytest
        echo "review OK"
        """,
    )

    write(
        FLOW / ".pre-commit-config.yaml",
        """
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.15.12
            hooks:
              - id: ruff
                args: ["check", "--fix"]
                files: ^tooling/
        """,
    )

    write(
        FLOW / ".github/workflows/ci.yml",
        """
        name: ci

        on:
          push:
            branches: [main, master]
          pull_request:

        jobs:
          quality:
            runs-on: ubuntu-latest
            defaults:
              run:
                working-directory: tooling
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v5
                with:
                  python-version: "3.12"
                  cache: pip
                  cache-dependency-path: tooling/requirements-dev.txt
              - name: Install dev tools
                run: |
                  python -m pip install -U pip
                  pip install -r requirements-dev.txt
              - name: Ruff
                run: ruff check .
              - name: Bandit
                run: bandit -q -c pyproject.toml -r . -x ./.venv
              - name: Pytest
                run: pytest

          semgrep:
            name: semgrep
            runs-on: ubuntu-latest
            container:
              image: returntocorp/semgrep
            steps:
              - uses: actions/checkout@v4
              - name: Semgrep
                run: semgrep ci --config p/python --error tooling
        """,
    )

    print("bootstrap done")


if __name__ == "__main__":
    main()
