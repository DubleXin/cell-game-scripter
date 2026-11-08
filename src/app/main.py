from collections.abc import Callable

from app.src.engine.engine import Engine, EngineError
from app.src.models.grid import Grid
from app.src.models.simulation import Simulation
from app.src.ui.app import App


def main() -> None:
    engine: Engine = Engine()

    simulation: Simulation | None = None

    def get_simulation() -> Simulation | None:
        return simulation

    def set_simulation(
        initial_grid: Grid,
        generation_count: int,
    ) -> bool:
        nonlocal simulation

        try:
            simulation = engine.run(
                initial_grid=initial_grid,
                generation_count=generation_count,
            )
        except EngineError:
            return False

        return True

    initial_grid: Grid = Grid(
        width=5,
        height=5,
        cells=[
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
    )

    # Temporary initial state until SetupTab is ready.
    set_simulation(
        initial_grid=initial_grid,
        generation_count=25,
    )

    app = App(
        get_simulation=get_simulation,
        set_simulation=set_simulation,
    )

    app.run()


if __name__ == "__main__":
    main()
