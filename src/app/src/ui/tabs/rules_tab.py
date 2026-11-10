import tkinter as tk
from collections.abc import Callable
from tkinter import IntVar, StringVar, ttk

from app.src.models.rule import Rule, RuleType
from app.src.ui.tabs.tab import Tab
from app.src.ui.widgets.rule_editor_row import RuleEditorRow


class RulesTab(Tab):
    MIN_NEIGHBORHOOD_SIZE = 3
    MAX_NEIGHBORHOOD_SIZE = 9

    def __init__(
        self,
        notebook: ttk.Notebook,
    ) -> None:
        super().__init__(
            notebook,
            title="Rules",
        )

        self.neighborhood_size = IntVar(value=self.MIN_NEIGHBORHOOD_SIZE)
        self.status_text = StringVar(value="Status: —")

        self.rule_rows: list[RuleEditorRow] = []

        self.neighborhood_input: ttk.Spinbox
        self.apply_button: ttk.Button

        self.rules_canvas: tk.Canvas
        self.rules_frame: ttk.Frame

    def build(self) -> None:
        self.frame.columnconfigure(
            0,
            weight=1,
        )

        # Rules list takes all free vertical space.
        self.frame.rowconfigure(
            2,
            weight=1,
        )

        # ---------------- Settings ----------------

        settings_frame = ttk.Frame(
            self.frame,
            padding=(0, 0, 0, 10),
        )
        settings_frame.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        settings_frame.columnconfigure(
            1,
            weight=1,
        )

        neighborhood_label = ttk.Label(
            settings_frame,
            text="Neighborhood size",
        )
        neighborhood_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
        )

        self.neighborhood_input = ttk.Spinbox(
            settings_frame,
            from_=self.MIN_NEIGHBORHOOD_SIZE,
            to=self.MAX_NEIGHBORHOOD_SIZE,
            increment=2,
            textvariable=self.neighborhood_size,
        )
        self.neighborhood_input.grid(
            row=0,
            column=1,
            sticky="ew",
        )

        # ---------------- Add rule buttons ----------------

        buttons_frame = ttk.Frame(
            self.frame,
        )
        buttons_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )

        population_button = ttk.Button(
            buttons_frame,
            text="Add Population Rule",
            command=lambda: self.add_rule(RuleType.POPULATION),
        )
        population_button.pack(
            side="left",
            padx=(0, 5),
        )

        neighbor_button = ttk.Button(
            buttons_frame,
            text="Add Neighbor Rule",
            command=lambda: self.add_rule(RuleType.NEIGHBOR),
        )
        neighbor_button.pack(
            side="left",
        )

        # ---------------- Scrollable rules area ----------------

        rules_container = ttk.Frame(
            self.frame,
        )
        rules_container.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        rules_container.rowconfigure(
            0,
            weight=1,
        )
        rules_container.columnconfigure(
            0,
            weight=1,
        )

        self.rules_canvas = tk.Canvas(
            rules_container,
            highlightthickness=0,
        )
        self.rules_canvas.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scrollbar = ttk.Scrollbar(
            rules_container,
            orient="vertical",
            command=self.rules_canvas.yview,
        )
        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        self.rules_canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        self.rules_frame = ttk.Frame(
            self.rules_canvas,
            padding=10,
        )

        rules_window = self.rules_canvas.create_window(
            (0, 0),
            window=self.rules_frame,
            anchor="nw",
        )

        self.rules_frame.bind(
            "<Configure>",
            lambda _: self.rules_canvas.configure(
                scrollregion=self.rules_canvas.bbox("all")
            ),
        )

        self.rules_canvas.bind(
            "<Configure>",
            lambda event: self.rules_canvas.itemconfigure(
                rules_window,
                width=event.width,
            ),
        )

        self.rules_frame.columnconfigure(
            0,
            weight=1,
        )

        # ---------------- Apply ----------------

        self.apply_button = ttk.Button(
            self.frame,
            text="Apply",
        )
        self.apply_button.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(10, 0),
        )

        status_label = ttk.Label(
            self.frame,
            textvariable=self.status_text,
        )
        status_label.grid(
            row=4,
            column=0,
            sticky="w",
            pady=(5, 0),
        )

    def bind_apply(
        self,
        fn: Callable[[], None],
    ) -> None:
        self.apply_button.configure(
            command=fn,
        )

    def add_rule(
        self,
        rule_type: RuleType,
        initial_rule: Rule | None = None,
    ) -> None:
        row = RuleEditorRow(
            parent=self.rules_frame,
            rule_type=rule_type,
            get_neighborhood_size=self.get_neighborhood_size,
            on_delete=self._delete_rule,
            initial_rule=initial_rule,
        )

        self.rule_rows.append(row)

        self._rebuild_rule_rows()

    def _delete_rule(
        self,
        row: RuleEditorRow,
    ) -> None:
        row.frame.destroy()

        self.rule_rows.remove(row)

        self._rebuild_rule_rows()

    def _rebuild_rule_rows(self) -> None:
        for index, row in enumerate(self.rule_rows):
            row.frame.grid(
                row=index,
                column=0,
                sticky="ew",
                pady=4,
            )

    def get_rules(self) -> list[Rule]:
        return [row.get_rule() for row in self.rule_rows]

    def set_rules(
        self,
        rules: list[Rule],
    ) -> None:
        for row in self.rule_rows:
            row.frame.destroy()

        self.rule_rows.clear()

        for rule in rules:
            self.add_rule(
                rule.rule_type,
                initial_rule=rule,
            )

    def get_neighborhood_size(self) -> int:
        try:
            value = int(self.neighborhood_input.get())
        except ValueError:
            value = self.MIN_NEIGHBORHOOD_SIZE

        value = max(
            self.MIN_NEIGHBORHOOD_SIZE,
            min(
                self.MAX_NEIGHBORHOOD_SIZE,
                value,
            ),
        )

        if value % 2 == 0:
            value -= 1

        self.neighborhood_size.set(value)

        return value

    def set_neighborhood_size(
        self,
        value: int,
    ) -> None:
        self.neighborhood_size.set(value)

    def set_status(
        self,
        status: str,
    ) -> None:
        self.status_text.set(f"Status: {status}")
