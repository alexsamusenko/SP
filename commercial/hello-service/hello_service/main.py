"""Минимальный пример приложения под `commercial/`."""


def greet(where: str = "Flow") -> str:
    return f"Hello from {where}"


def main() -> None:
    print(greet())


if __name__ == "__main__":
    main()
