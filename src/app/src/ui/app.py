from collections.abc import Callable
from tkinter import Tk

from app.src.models.grid import Grid
from app.src.models.simulation import Simulation
from app.src.ui.app_ui import AppUI
from app.src.ui.controllers.setup_controller import SetupController
from app.src.ui.controllers.simulation_controller import SimulationController


class App:
    def __init__(
        self,
        get_simulation: Callable[
            [],
            Simulation | None,
        ],
        set_simulation: Callable[
            [Grid, int],
            bool,
        ],
    ) -> None:
        self.get_simulation = get_simulation
        self.set_simulation = set_simulation

        self.root: Tk | None = None
        self.appui: AppUI | None = None

        self.setup_controller: SetupController | None = None
        self.simulation_controller: SimulationController | None = None

    def run(self) -> None:
        self.root = Tk()

        self.root.title("Cell Game Scripter")
        self.root.geometry("700x700")

        self.appui = AppUI(self.root)

        self.simulation_controller = SimulationController(
            root=self.root,
            tab=self.appui.simulation_tab,
            get_simulation=self.get_simulation,
        )

        self.setup_controller = SetupController(
            tab=self.appui.setup_tab,
            set_simulation=self.set_simulation,
            on_simulation_ready=(self.simulation_controller.reset),
        )

        self.simulation_controller.bind()
        self.setup_controller.bind()

        self.simulation_controller.render_current()

        self.root.after_idle(self.setup_controller.apply_setup)

        self.root.mainloop()
