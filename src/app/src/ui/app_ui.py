import tkinter as tk
from tkinter import ttk

from app.src.ui.tabs.rules_tab import RulesTab
from app.src.ui.tabs.setup_tab import SetupTab
from app.src.ui.tabs.simulation_tab import SimulationTab


class AppUI:
    def __init__(
        self,
        root: tk.Tk,
    ) -> None:
        self.root = root

        self.root.rowconfigure(
            0,
            weight=1,
        )
        self.root.columnconfigure(
            0,
            weight=1,
        )

        self.main_frame = ttk.Frame(
            root,
            padding=12,
        )
        self.main_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.main_frame.rowconfigure(
            0,
            weight=1,
        )
        self.main_frame.columnconfigure(
            0,
            weight=1,
        )

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.setup_tab = SetupTab(self.notebook)
        self.simulation_tab = SimulationTab(self.notebook)
        self.rules_tab = RulesTab(self.notebook)

        self.setup_tab.build()
        self.simulation_tab.build()
        self.rules_tab.build()
