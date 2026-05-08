import pytest

from guard import safe_snippet


def test_safe_accepts_normal_text() -> None:
    assert "hello" in safe_snippet("hello world")


def test_safe_blocks_secrets() -> None:
    with pytest.raises(ValueError):
        safe_snippet("-----BEGIN PRIVATE KEY-----\nMIIE...")
