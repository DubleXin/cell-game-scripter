import os


def write(
    data_path: str,
    grid: tuple[int, int],
    max_generations: int,
    initial_state: list[int],
) -> None:
    os.makedirs(data_path, exist_ok=True)
    with open(os.path.join(data_path, ".input"), "w") as f:
        f.write(f"{grid[0]}\n{grid[1]}\n{max_generations}\n{initial_state}")
