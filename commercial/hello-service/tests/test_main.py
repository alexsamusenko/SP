from hello_service.main import greet


def test_greet_contains_flow() -> None:
    assert "Flow" in greet()


def test_greet_custom() -> None:
    assert greet("demo") == "Hello from demo"
