import tkinter as tk
from tkinter import ttk


class Tab:
    def __init__(
        self,
        notebook: ttk.Notebook,
        title: str,
    ) -> None:
        self.frame = ttk.Frame(
            notebook,
            padding=12,
        )

        notebook.add(
            self.frame,
            text=title,
        )

    def build(self) -> None:
        raise NotImplementedError("Tab subclasses must implement build()")
