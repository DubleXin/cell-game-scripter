import tkinter as tk
from collections.abc import Callable
from tkinter import DoubleVar, StringVar, ttk

from app.src.models.grid import Grid
from app.src.ui.helpers.render_grid import render_grid
from app.src.ui.tabs.tab import Tab


class SimulationTab(Tab):
    MIN_SPEED = 1.0
    MAX_SPEED = 20.0
    DEFAULT_SPEED = 4.0

    def __init__(
        self,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(
            notebook,
            title="Simulation",
        )

        self.generation_text = StringVar(value="Generation: 0")

        self.speed_value = DoubleVar(value=self.DEFAULT_SPEED)

        self.speed_text = StringVar(value=f"Speed: {self.DEFAULT_SPEED:.0f}x")

        self.canvas: tk.Canvas

        self.previous_button: ttk.Button
        self.run_button: ttk.Button
        self.next_button: ttk.Button
        self.reset_button: ttk.Button

        self.speed_scale: ttk.Scale

    def build(self) -> None:
        self.frame.rowconfigure(
            1,
            weight=1,
        )

        for column in range(4):
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
            columnspan=4,
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
            columnspan=4,
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
            text="Play",
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
            padx=5,
        )

        self.reset_button = ttk.Button(
            self.frame,
            text="Reset",
        )
        self.reset_button.grid(
            row=2,
            column=3,
            sticky="ew",
            padx=(5, 0),
        )

        speed_label = ttk.Label(
            self.frame,
            textvariable=self.speed_text,
        )
        speed_label.grid(
            row=3,
            column=0,
            pady=(15, 0),
        )

        self.speed_scale = ttk.Scale(
            self.frame,
            from_=self.MIN_SPEED,
            to=self.MAX_SPEED,
            variable=self.speed_value,
        )
        self.speed_scale.grid(
            row=3,
            column=1,
            columnspan=3,
            sticky="ew",
            pady=(15, 0),
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

    def bind_reset(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.reset_button.configure(command=fn)

    def bind_speed_change(
        self,
        fn: Callable[[float], None],
    ) -> None:
        def on_change(value: str) -> None:
            speed = float(value)

            self.speed_text.set(f"Speed: {speed:.1f}x")

            fn(speed)

        self.speed_scale.configure(command=on_change)

    def set_run_state(
        self,
        is_playing: bool,
    ) -> None:
        self.run_button.configure(text="Pause" if is_playing else "Play")

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
