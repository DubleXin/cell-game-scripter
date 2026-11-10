from collections.abc import Callable

from app.src.models.grid import Grid
from app.src.ui.tabs.setup_tab import SetupTab


class SetupController:
    def __init__(
        self,
        tab: SetupTab,
        set_simulation: Callable[[Grid, int], bool],
        on_simulation_ready: Callable[[], None],
    ) -> None:
        self.tab = tab
        self.set_simulation = set_simulation
        self.on_simulation_ready = on_simulation_ready

        self.setup_grid: Grid | None = None
        self.setup_max_sims: int = 10

    def bind(self) -> None:
        self.tab.bind_apply(self.apply_setup)

        self.tab.bind_run(self.send_simulation_data)

        self.tab.bind_cell_click(self.on_cell_click)

    def apply_setup(self) -> None:
        width: int = self.tab.get_width()
        height: int = self.tab.get_height()

        self.setup_max_sims = self.tab.get_max_sims()

        self.setup_grid = Grid(
            width=width,
            height=height,
            cells=[0 for _ in range(width * height)],
        )

        self.tab.set_status("—")

        self.tab.render_grid(self.setup_grid)

    def send_simulation_data(self) -> None:
        if self.setup_grid is None:
            return

        success: bool = self.set_simulation(
            self.setup_grid,
            self.setup_max_sims,
        )

        if not success:
            self.tab.set_status("ERROR")
            return

        self.tab.set_status("OK")

        self.on_simulation_ready()

    def on_cell_click(
        self,
        x: int,
        y: int,
    ) -> None:
        if self.setup_grid is None:
            return

        index: int = y * self.setup_grid.width + x

        self.setup_grid.cells[index] = 0 if self.setup_grid.cells[index] == 1 else 1

        self.tab.render_grid(self.setup_grid)
