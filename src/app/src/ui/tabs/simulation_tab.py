import tkinter as tk
from collections.abc import Callable
from tkinter import StringVar, ttk

from app.src.models.grid import Grid
from app.src.ui.helpers.render_grid import render_grid
from app.src.ui.tabs.tab import Tab


class SimulationTab(Tab):
    def __init__(
        self,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(
            notebook,
            title="Simulation",
        )

        self.generation_text = StringVar(value="Generation: 0")

        self.canvas: tk.Canvas
        self.previous_button: ttk.Button
        self.run_button: ttk.Button
        self.next_button: ttk.Button

    def build(self) -> None:
        self.frame.rowconfigure(
            1,
            weight=1,
        )

        for column in range(3):
            self.frame.columnconfigure(
                column,
                weight=1,
            )

        generation_label = ttk.Label(
            self.frame,
            textvariable=self.generation_text,
        )
        generation_label.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=(0, 10),
        )

        self.canvas = tk.Canvas(
            self.frame,
            width=500,
            height=500,
            background="white",
        )
        self.canvas.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            pady=(0, 10),
        )

        self.previous_button = ttk.Button(
            self.frame,
            text="Previous",
        )
        self.previous_button.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        self.run_button = ttk.Button(
            self.frame,
            text="Run",
        )
        self.run_button.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=5,
        )

        self.next_button = ttk.Button(
            self.frame,
            text="Next",
        )
        self.next_button.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=(5, 0),
        )

    def bind_run(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.run_button.configure(command=fn)

    def bind_previous(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.previous_button.configure(command=fn)

    def bind_next(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.next_button.configure(command=fn)

    def set_generation(
        self,
        generation: int,
    ) -> None:
        self.generation_text.set(f"Generation: {generation}")

    def render_grid(
        self,
        grid: Grid,
    ) -> None:
        render_grid(
            self.canvas,
            grid,
        )
