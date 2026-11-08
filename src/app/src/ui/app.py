from collections.abc import Callable
from tkinter import Tk

from app.src.models.grid import Grid
from app.src.models.simulation import Simulation
from app.src.ui.app_ui import AppUI
from app.src.ui.controllers.button_controller import (
    on_next,
    on_previous,
)


class App:
    def __init__(
        self,
        get_simulation: Callable[[], Simulation | None],
        set_simulation: Callable[
            [Grid, int],
            bool,
        ],
    ) -> None:
        self.current_generation: int = 0
        self.setup_max_sims: int = 10
        self.get_simulation = get_simulation
        self.set_simulation = set_simulation
        self.setup_grid: Grid | None = None

        self.root: Tk | None = None
        self.appui: AppUI | None = None

        self.is_playing: bool = False
        self.after_id: str | None = None

    def run(self) -> None:
        self.root = Tk()

        self.root.title("Cell Game Scripter")
        self.root.geometry("700x700")

        self.appui = AppUI(self.root)

        # ---------------------------------------------

        setup_tab = self.appui.setup_tab

        setup_tab.bind_apply(self._apply_setup)

        setup_tab.bind_run(self._send_simulation_data)

        setup_tab.bind_cell_click(self._on_setup_cell_click)
        # ---------------------------------------------

        simulation_tab = self.appui.simulation_tab

        simulation_tab.bind_next(lambda: on_next(self._change_generation))

        simulation_tab.bind_previous(lambda: on_previous(self._change_generation))

        simulation_tab.bind_run(self._on_run)

        # ---------------------------------------------

        self._render_current_generation()

        self.root.after_idle(self._apply_setup)

        self.root.mainloop()

    def _change_generation(
        self,
        modifier: int,
    ) -> None:
        new_generation: int = self.current_generation + modifier

        if not (0 <= new_generation < len(self.get_simulation())):
            return

        self.current_generation = new_generation

        self._render_current_generation()

    def _render_current_generation(
        self,
    ) -> None:
        if self.appui is None:
            return

        simulation_tab = self.appui.simulation_tab

        simulation_tab.set_generation(self.current_generation)

        simulation_tab.render_grid(self.get_simulation()[self.current_generation])

    def _on_run(self) -> None:
        if self.root is None:
            return

        if self.is_playing:
            self.is_playing = False

            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            return

        self.is_playing = True

        if self.current_generation >= len(self.get_simulation()) - 1:
            self.current_generation = 0
            self._render_current_generation()

        self._play_next_generation()

    def _play_next_generation(self) -> None:
        if self.root is None or self.appui is None:
            return

        if not self.is_playing:
            return

        if self.current_generation >= len(self.get_simulation()) - 1:
            self.is_playing = False
            self.after_id = None
            return

        self.current_generation += 1
        self._render_current_generation()

        self.after_id = self.root.after(
            250,
            self._play_next_generation,
        )

    def _apply_setup(self) -> None:
        if self.appui is None:
            return

        setup_tab = self.appui.setup_tab

        width: int = setup_tab.get_width()
        height: int = setup_tab.get_height()

        self.setup_max_sims = setup_tab.get_max_sims()

        self.setup_grid = Grid(
            width=width,
            height=height,
            cells=[0 for _ in range(width * height)],
        )

        setup_tab.render_grid(self.setup_grid)

    def _send_simulation_data(self) -> None:
        if self.setup_grid is None or self.appui is None:
            return

        success: bool = self.set_simulation(
            self.setup_grid,
            self.setup_max_sims,
        )

        if success:
            self.appui.setup_tab.set_status("OK")
        else:
            self.appui.setup_tab.set_status("ERROR")

    def _on_setup_cell_click(
        self,
        x: int,
        y: int,
    ) -> None:
        if self.setup_grid is None or self.appui is None:
            return

        index: int = y * self.setup_grid.width + x

        self.setup_grid.cells[index] = 0 if self.setup_grid.cells[index] == 1 else 1

        self.appui.setup_tab.render_grid(self.setup_grid)
