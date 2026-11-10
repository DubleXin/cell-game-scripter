from collections.abc import Callable
from tkinter import StringVar, ttk

from app.src.models.rule import (
    CellState,
    ComparisonType,
    Rule,
    RuleType,
)


class RuleEditorRow:
    def __init__(
        self,
        parent: ttk.Frame,
        rule_type: RuleType,
        get_neighborhood_size: Callable[[], int],
        on_delete: Callable[["RuleEditorRow"], None],
        initial_rule: Rule | None = None,
    ) -> None:
        self.rule_type = rule_type
        self.get_neighborhood_size = get_neighborhood_size
        self.on_delete = on_delete

        self.frame = ttk.Frame(
            parent,
            padding=8,
            relief="groove",
        )

        self.target_value = StringVar(value="1")
        self.comparison_value = StringVar(value="==")
        self.result_value = StringVar(value="0")

        self.arg_value = StringVar(value="0")
        self.position_value = StringVar(value="0_0")

        self.status_value = StringVar(value="")

        self._build()

        if initial_rule is not None:
            self.set_rule(initial_rule)

    def _build(self) -> None:
        column = 0

        ttk.Label(
            self.frame,
            text="Cell",
        ).grid(
            row=0,
            column=column,
            padx=4,
        )
        column += 1

        ttk.Combobox(
            self.frame,
            textvariable=self.target_value,
            values=("0", "1"),
            state="readonly",
            width=4,
        ).grid(
            row=0,
            column=column,
            padx=4,
        )
        column += 1

        ttk.Label(
            self.frame,
            text=(
                "Population" if self.rule_type == RuleType.POPULATION else "Neighbor"
            ),
        ).grid(
            row=0,
            column=column,
            padx=8,
        )
        column += 1

        if self.rule_type == RuleType.NEIGHBOR:
            ttk.Entry(
                self.frame,
                textvariable=self.position_value,
                width=7,
            ).grid(
                row=0,
                column=column,
                padx=4,
            )
            column += 1

        ttk.Combobox(
            self.frame,
            textvariable=self.comparison_value,
            values=("==", ">", "<"),
            state="readonly",
            width=4,
        ).grid(
            row=0,
            column=column,
            padx=4,
        )
        column += 1

        if self.rule_type == RuleType.POPULATION:
            ttk.Entry(
                self.frame,
                textvariable=self.arg_value,
                width=7,
            ).grid(
                row=0,
                column=column,
                padx=4,
            )
        else:
            ttk.Combobox(
                self.frame,
                textvariable=self.arg_value,
                values=("0", "1"),
                state="readonly",
                width=4,
            ).grid(
                row=0,
                column=column,
                padx=4,
            )

        column += 1

        ttk.Label(
            self.frame,
            text="→",
        ).grid(
            row=0,
            column=column,
            padx=4,
        )
        column += 1

        ttk.Combobox(
            self.frame,
            textvariable=self.result_value,
            values=("0", "1"),
            state="readonly",
            width=4,
        ).grid(
            row=0,
            column=column,
            padx=4,
        )
        column += 1

        ttk.Button(
            self.frame,
            text="Save",
            command=self.save,
        ).grid(
            row=0,
            column=column,
            padx=(8, 4),
        )
        column += 1

        ttk.Button(
            self.frame,
            text="✕",
            width=3,
            command=lambda: self.on_delete(self),
        ).grid(
            row=0,
            column=column,
            padx=4,
        )

        ttk.Label(
            self.frame,
            textvariable=self.status_value,
        ).grid(
            row=1,
            column=0,
            columnspan=column + 1,
            sticky="w",
            pady=(5, 0),
        )

    def save(self) -> None:
        try:
            self.get_rule()
        except ValueError as error:
            self.status_value.set(f"Error: {error}")
            return

        self.status_value.set("Saved")

    def get_rule(self) -> Rule:
        neighborhood_size = self.get_neighborhood_size()

        target_state = CellState(int(self.target_value.get()))

        result = CellState(int(self.result_value.get()))

        comparison = self._get_comparison()

        if self.rule_type == RuleType.POPULATION:
            try:
                population = int(self.arg_value.get())
            except ValueError:
                raise ValueError("population must be an integer")

            max_population = neighborhood_size * neighborhood_size - 1

            if not 0 <= population <= max_population:
                raise ValueError(f"population must be 0..{max_population}")

            args = [population]

        else:
            position = self._get_position(neighborhood_size)

            neighbor_state = CellState(int(self.arg_value.get()))

            args = [
                position,
                neighbor_state,
            ]

        return Rule(
            target_state=target_state,
            rule_type=self.rule_type,
            comparison=comparison,
            result=result,
            args=args,
        )

    def _get_comparison(
        self,
    ) -> ComparisonType:
        value = self.comparison_value.get()

        if value == "==":
            return ComparisonType.EQUAL

        if value == ">":
            return ComparisonType.GREATER

        if value == "<":
            return ComparisonType.LESS

        raise ValueError("invalid comparison")

    def _get_position(
        self,
        neighborhood_size: int,
    ) -> tuple[int, int]:
        parts = self.position_value.get().split("_")

        if len(parts) != 2:
            raise ValueError("position must use x_y format")

        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError:
            raise ValueError("position must use integer coordinates")

        if not (0 <= x < neighborhood_size and 0 <= y < neighborhood_size):
            raise ValueError("neighbor is outside neighborhood")

        center = neighborhood_size // 2

        if x == center and y == center:
            raise ValueError("neighbor cannot be the target cell")

        return x, y

    def set_rule(
        self,
        rule: Rule,
    ) -> None:
        self.target_value.set(str(int(rule.target_state)))

        self.result_value.set(str(int(rule.result)))

        comparisons = {
            ComparisonType.EQUAL: "==",
            ComparisonType.GREATER: ">",
            ComparisonType.LESS: "<",
        }

        self.comparison_value.set(comparisons[rule.comparison])

        if rule.rule_type == RuleType.POPULATION:
            self.arg_value.set(str(rule.args[0]))

        else:
            x, y = rule.args[0]

            self.position_value.set(f"{x}_{y}")

            self.arg_value.set(str(int(rule.args[1])))
