from collections.abc import Callable


def on_next(change_generation: Callable[[int], None]) -> None:
    change_generation(1)


def on_previous(change_generation: Callable[[int], None]) -> None:
    change_generation(-1)
