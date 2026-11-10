from collections.abc import Callable
from tkinter import Tk

from app.src.models.simulation import Simulation
from app.src.ui.tabs.simulation_tab import SimulationTab


class SimulationController:
    def __init__(
        self,
        root: Tk,
        tab: SimulationTab,
        get_simulation: Callable[[], Simulation | None],
    ) -> None:
        self.root = root
        self.tab = tab
        self.get_simulation = get_simulation

        self.current_generation: int = 0

        self.is_playing: bool = False
        self.after_id: str | None = None

        self.playback_delay_ms: int = 250

    def bind(self) -> None:
        self.tab.bind_next(lambda: self.change_generation(1))

        self.tab.bind_previous(lambda: self.change_generation(-1))

        self.tab.bind_run(self.toggle_playback)

        self.tab.bind_reset(self.reset)

        self.tab.bind_speed_change(self.change_speed)

    def change_generation(
        self,
        modifier: int,
    ) -> None:
        simulation = self.get_simulation()

        if simulation is None:
            return

        new_generation: int = self.current_generation + modifier

        if not (0 <= new_generation < len(simulation)):
            return

        self.current_generation = new_generation

        self.render_current()

    def render_current(self) -> None:
        simulation = self.get_simulation()

        if simulation is None:
            return

        self.tab.set_generation(self.current_generation)

        self.tab.render_grid(simulation[self.current_generation])

    def toggle_playback(self) -> None:
        simulation = self.get_simulation()

        if simulation is None:
            return

        if self.is_playing:
            self.stop_playback()
            return

        if self.current_generation >= len(simulation) - 1:
            self.current_generation = 0
            self.render_current()

        self.is_playing = True

        self.tab.set_run_state(True)

        self._play_next_generation()

    def stop_playback(self) -> None:
        self.is_playing = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.tab.set_run_state(False)

    def reset(self) -> None:
        simulation = self.get_simulation()

        if simulation is None:
            return

        self.stop_playback()

        self.current_generation = 0

        self.render_current()

    def change_speed(
        self,
        speed: float,
    ) -> None:
        if speed <= 0:
            return

        self.playback_delay_ms = int(1000 / speed)

    def _play_next_generation(self) -> None:
        simulation = self.get_simulation()

        if simulation is None:
            self.stop_playback()
            return

        if not self.is_playing:
            return

        if self.current_generation >= len(simulation) - 1:
            self.stop_playback()
            return

        self.current_generation += 1

        self.render_current()

        self.after_id = self.root.after(
            self.playback_delay_ms,
            self._play_next_generation,
        )
