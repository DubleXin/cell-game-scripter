import tkinter as tk
from collections.abc import Callable
from tkinter import IntVar, StringVar, ttk

from app.src.models.grid import Grid
from app.src.ui.helpers.render_grid import render_grid
from app.src.ui.tabs.tab import Tab


class SetupTab(Tab):
    MIN_GRID_SIZE = 3
    MAX_GRID_SIZE = 100

    MIN_SIMULATIONS = 1
    MAX_SIMULATIONS = 1000

    def __init__(
        self,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(
            notebook,
            title="Setup",
        )

        self.width_value = IntVar(value=self.MIN_GRID_SIZE)
        self.height_value = IntVar(value=self.MIN_GRID_SIZE)
        self.max_sims_value = IntVar(value=100)

        self.status_text = StringVar(value="Status: —")

        self.canvas: tk.Canvas

        self.width_input: ttk.Spinbox
        self.height_input: ttk.Spinbox
        self.max_sims_input: ttk.Spinbox

        self.apply_button: ttk.Button
        self.run_button: ttk.Button

        self._grid_width: int = 0
        self._grid_height: int = 0

        self._cell_click_callback: Callable[[int, int], None] | None = None

    def build(self) -> None:
        self.frame.columnconfigure(
            0,
            weight=3,
        )
        self.frame.columnconfigure(
            1,
            weight=1,
        )
        self.frame.rowconfigure(
            0,
            weight=1,
        )

        self.canvas = tk.Canvas(
            self.frame,
            width=600,
            height=600,
            background="white",
        )
        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12),
        )

        controls = ttk.Frame(
            self.frame,
            padding=12,
        )
        controls.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        controls.columnconfigure(
            0,
            weight=1,
        )

        title = ttk.Label(
            controls,
            text="Grid Setup",
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 20),
        )

        width_label = ttk.Label(
            controls,
            text="Width",
        )
        width_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        self.width_input = ttk.Spinbox(
            controls,
            from_=self.MIN_GRID_SIZE,
            to=self.MAX_GRID_SIZE,
            textvariable=self.width_value,
        )
        self.width_input.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        height_label = ttk.Label(
            controls,
            text="Height",
        )
        height_label.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        self.height_input = ttk.Spinbox(
            controls,
            from_=self.MIN_GRID_SIZE,
            to=self.MAX_GRID_SIZE,
            textvariable=self.height_value,
        )
        self.height_input.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        max_sims_label = ttk.Label(
            controls,
            text="Generations",
        )
        max_sims_label.grid(
            row=5,
            column=0,
            sticky="w",
            pady=(0, 5),
        )

        self.max_sims_input = ttk.Spinbox(
            controls,
            from_=self.MIN_SIMULATIONS,
            to=self.MAX_SIMULATIONS,
            textvariable=self.max_sims_value,
        )
        self.max_sims_input.grid(
            row=6,
            column=0,
            sticky="ew",
            pady=(0, 15),
        )

        self.apply_button = ttk.Button(
            controls,
            text="Apply",
        )
        self.apply_button.grid(
            row=7,
            column=0,
            sticky="ew",
        )

        controls.rowconfigure(
            8,
            weight=1,
        )

        self.run_button = ttk.Button(
            controls,
            text="Run Simulation",
        )
        self.run_button.grid(
            row=9,
            column=0,
            sticky="ew",
            pady=(20, 10),
        )

        status_label = ttk.Label(
            controls,
            textvariable=self.status_text,
        )
        status_label.grid(
            row=10,
            column=0,
            sticky="w",
        )

    def bind_apply(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.apply_button.configure(
            command=fn,
        )

    def bind_run(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.run_button.configure(
            command=fn,
        )

    def get_width(self) -> int:
        return self._get_int_value(
            self.width_input,
            self.width_value,
            self.MIN_GRID_SIZE,
            self.MAX_GRID_SIZE,
        )

    def get_height(self) -> int:
        return self._get_int_value(
            self.height_input,
            self.height_value,
            self.MIN_GRID_SIZE,
            self.MAX_GRID_SIZE,
        )

    def get_max_sims(self) -> int:
        return self._get_int_value(
            self.max_sims_input,
            self.max_sims_value,
            self.MIN_SIMULATIONS,
            self.MAX_SIMULATIONS,
        )

    def _get_int_value(
        self,
        input_field: ttk.Spinbox,
        variable: IntVar,
        minimum: int,
        maximum: int,
    ) -> int:
        try:
            value = int(input_field.get())
        except ValueError:
            value = minimum

        value = max(
            minimum,
            min(maximum, value),
        )

        variable.set(value)

        return value

    def render_grid(
        self,
        grid: Grid,
    ) -> None:
        self._grid_width = grid.width
        self._grid_height = grid.height

        render_grid(
            self.canvas,
            grid,
        )

    def set_status(
        self,
        status: str,
    ) -> None:
        self.status_text.set(f"Status: {status}")

    def bind_cell_click(
        self,
        fn: Callable[[int, int], None],
    ) -> None:
        self._cell_click_callback = fn

        self.canvas.bind(
            "<Button-1>",
            self._on_canvas_click,
        )

    def _on_canvas_click(
        self,
        event: tk.Event,
    ) -> None:
        if (
            self._cell_click_callback is None
            or self._grid_width <= 0
            or self._grid_height <= 0
        ):
            return

        canvas_width: int = self.canvas.winfo_width()
        canvas_height: int = self.canvas.winfo_height()

        cell_width: float = canvas_width / self._grid_width
        cell_height: float = canvas_height / self._grid_height

        x: int = int(event.x / cell_width)
        y: int = int(event.y / cell_height)

        if not (0 <= x < self._grid_width and 0 <= y < self._grid_height):
            return

        self._cell_click_callback(
            x,
            y,
        )
