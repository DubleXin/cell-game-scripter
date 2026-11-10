from tkinter import ttk

from app.src.ui.tabs.tab import Tab


class RulesTab(Tab):
    def __init__(
        self,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(
            notebook,
            title="Rules",
        )

    def build(self) -> None:
        label = ttk.Label(
            self.frame,
            text="Rule editor",
        )

        label.grid(
            row=0,
            column=0,
        )
