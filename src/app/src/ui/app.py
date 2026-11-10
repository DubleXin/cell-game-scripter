from collections.abc import Callable
from tkinter import Tk

from app.src.models.grid import Grid
from app.src.models.rule import Rule
from app.src.models.simulation import Simulation
from app.src.ui.app_ui import AppUI
from app.src.ui.controllers.rules_controller import RulesController
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
        get_rules: Callable[[], list[Rule]],
        get_neighborhood_size: Callable[[], int],
        set_rules: Callable[[list[Rule], int], None],
    ) -> None:
        self.get_simulation = get_simulation
        self.set_simulation = set_simulation
        self.get_rules = get_rules
        self.get_neighborhood_size = get_neighborhood_size
        self.set_rules = set_rules

        self.root: Tk | None = None
        self.appui: AppUI | None = None

        self.setup_controller: SetupController | None = None
        self.simulation_controller: SimulationController | None = None
        self.rules_controller: RulesController | None = None

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

        self.rules_controller = RulesController(
            tab=self.appui.rules_tab,
            get_rules=self.get_rules,
            get_neighborhood_size=self.get_neighborhood_size,
            set_rules=self.set_rules,
        )

        self.rules_controller.bind()
        self.rules_controller.load()

        self.simulation_controller.bind()
        self.setup_controller.bind()

        self.simulation_controller.render_current()

        self.root.after_idle(self.setup_controller.apply_setup)

        self.root.mainloop()
