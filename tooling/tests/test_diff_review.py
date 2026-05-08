import pytest

from diff_review import clip_for_llm, get_diff_text


def test_clip_for_llm_truncates() -> None:
    long_diff = "a\n" * (30000 // 2)
    clipped = clip_for_llm(long_diff, max_chars=100)
    assert len(clipped) < len(long_diff)
    assert "обрезан" in clipped


def test_clip_for_llm_blocks_secrets() -> None:
    with pytest.raises(ValueError):
        clip_for_llm("-----BEGIN PRIVATE KEY-----\nMIIE", max_chars=1000)


def test_get_diff_text_runs_in_repo() -> None:
    s = get_diff_text(None)
    assert isinstance(s, str)
