FORBIDDEN = (".env", ".pem", "id_rsa", "aws_", "BEGIN PRIVATE")


def safe_snippet(text: str) -> str:
    lower = text.lower()
    if any(x in lower for x in FORBIDDEN):
        raise ValueError("blocked: похоже на секрет — не отправляем в LLM")
    return text
