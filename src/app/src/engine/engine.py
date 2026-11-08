import subprocess
import sys
from pathlib import Path

from app.src.models.grid import Grid
from app.src.models.simulation import Simulation
from app.src.serializer.read_output import read
from app.src.serializer.write_input import write


class EngineError(RuntimeError):
    pass


class Engine:
    def __init__(
        self,
        executable_path: str = "./build/engine",
        data_path: str = ".data",
    ) -> None:
        self.executable_path: Path = Path(executable_path)
        self.data_path: Path = Path(data_path)

    def run(
        self,
        initial_grid: Grid,
        generation_count: int,
    ) -> Simulation:
        if generation_count <= 0:
            raise ValueError("generation_count must be greater than 0")

        grid_size: tuple[int, int] = (
            initial_grid.width,
            initial_grid.height,
        )

        write(
            str(self.data_path),
            grid_size,
            generation_count,
            initial_grid.cells,
        )

        result: subprocess.CompletedProcess[str] = subprocess.run(
            [str(self.executable_path)],
            check=False,
            capture_output=True,
            text=True,
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")

        if result.returncode != 0:
            raise EngineError(f"Engine exited with code {result.returncode}")

        return read(str(self.data_path))
