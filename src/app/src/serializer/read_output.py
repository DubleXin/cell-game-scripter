from pathlib import Path

from app.src.models.grid import Grid
from app.src.models.simulation import Simulation


def read(data_path: str) -> Simulation:
    output_path: Path = Path(data_path) / ".output"

    with output_path.open("r", encoding="utf-8") as file:
        width: int = int(file.readline().strip())
        height: int = int(file.readline().strip())
        max_sims: int = int(file.readline().strip())

        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid grid size: {width}x{height}")

        if max_sims < 0:
            raise ValueError(f"Invalid max_sims: {max_sims}")

        snapshots: list[Grid] = []
        expected_gen: int = 0
        expected_cell_count: int = width * height

        while True:
            generation_line: str = file.readline()

            if not generation_line:
                break

            generation_line = generation_line.strip()

            if not generation_line:
                raise ValueError(
                    f"Missing generation number at generation {expected_gen}"
                )

            current_gen: int = int(generation_line)

            if current_gen != expected_gen:
                raise ValueError(
                    f"Expected generation {expected_gen}, got {current_gen}"
                )

            grid_line: str = file.readline()

            if not grid_line:
                raise ValueError(f"Missing grid data for generation {current_gen}")

            grid_line = grid_line.strip()

            if not grid_line.startswith("[") or not grid_line.endswith("]"):
                raise ValueError(f"Invalid grid format for generation {current_gen}")

            values: list[int] = [
                int(value.strip()) for value in grid_line[1:-1].split(",")
            ]

            if len(values) != expected_cell_count:
                raise ValueError(
                    f"Generation {current_gen} contains "
                    f"{len(values)} cells, expected {expected_cell_count}"
                )

            if any(value not in (0, 1) for value in values):
                raise ValueError(
                    f"Generation {current_gen} contains an invalid cell state"
                )

            snapshots.append(
                Grid(
                    width=width,
                    height=height,
                    cells=values,
                )
            )

            expected_gen += 1

        simulation: Simulation = Simulation(snapshots)

        expected_snapshot_count: int = max_sims + 1

        if len(simulation) != expected_snapshot_count:
            raise ValueError(
                f"Expected {expected_snapshot_count} snapshots "
                f"(generations 0-{max_sims}), got {len(simulation)}"
            )

        return simulation
