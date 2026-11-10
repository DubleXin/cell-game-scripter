from enum import IntEnum
from typing import TypeAlias


class CellState(IntEnum):
    DEAD = 0
    ALIVE = 1


class RuleType(IntEnum):
    POPULATION = 0
    NEIGHBOR = 1


class ComparisonType(IntEnum):
    EQUAL = 0
    GREATER = 1
    LESS = 2


NeighborPosition: TypeAlias = tuple[int, int]
RuleArg: TypeAlias = int | NeighborPosition


class Rule:
    def __init__(
        self,
        target_state: CellState,
        rule_type: RuleType,
        comparison: ComparisonType,
        result: CellState,
        args: list[RuleArg],
    ) -> None:
        self.target_state = target_state
        self.rule_type = rule_type
        self.comparison = comparison
        self.result = result
        self.args = args

        self._validate()

    def _validate(self) -> None:
        if self.rule_type == RuleType.POPULATION:
            if len(self.args) != 1:
                raise ValueError("Population rule requires exactly 1 argument")

            value = self.args[0]

            if not isinstance(value, int):
                raise ValueError("Population rule argument must be an integer")

            if value < 0:
                raise ValueError("Population value cannot be negative")

        elif self.rule_type == RuleType.NEIGHBOR:
            if len(self.args) != 2:
                raise ValueError("Neighbor rule requires exactly 2 arguments")

            position = self.args[0]
            value = self.args[1]

            if not (isinstance(position, tuple) and len(position) == 2):
                raise ValueError("Neighbor position must be (x, y)")

            if value not in (
                CellState.DEAD,
                CellState.ALIVE,
                0,
                1,
            ):
                raise ValueError("Neighbor state must be 0 or 1")
