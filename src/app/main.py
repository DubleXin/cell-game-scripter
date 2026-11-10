from app.src.engine.engine import Engine, EngineError
from app.src.models.grid import Grid
from app.src.models.rule import CellState, ComparisonType, Rule, RuleType
from app.src.models.simulation import Simulation
from app.src.ui.app import App


def main() -> None:
    engine: Engine = Engine()

    simulation: Simulation | None = None

    rules: list[Rule] = [
        # Alive cell dies with fewer than 2 neighbors.
        Rule(
            target_state=CellState.ALIVE,
            rule_type=RuleType.POPULATION,
            comparison=ComparisonType.LESS,
            result=CellState.DEAD,
            args=[2],
        ),
        # Alive cell dies with more than 3 neighbors.
        Rule(
            target_state=CellState.ALIVE,
            rule_type=RuleType.POPULATION,
            comparison=ComparisonType.GREATER,
            result=CellState.DEAD,
            args=[3],
        ),
        # Dead cell becomes alive with exactly 3 neighbors.
        Rule(
            target_state=CellState.DEAD,
            rule_type=RuleType.POPULATION,
            comparison=ComparisonType.EQUAL,
            result=CellState.ALIVE,
            args=[3],
        ),
    ]

    neighborhood_size: int = 3

    def get_simulation() -> Simulation | None:
        return simulation

    def set_simulation(
        initial_grid: Grid,
        generation_count: int,
    ) -> bool:
        nonlocal simulation

        try:
            simulation = engine.run(
                initial_grid=initial_grid,
                generation_count=generation_count,
                neighborhood_size=neighborhood_size,
                rules=rules,
            )
        except EngineError:
            return False

        return True

    def get_neighborhood_size() -> int:
        return neighborhood_size

    def get_rules() -> list[Rule]:
        return rules

    def set_rules(
        new_rules: list[Rule],
        new_neighborhood_size: int,
    ) -> None:
        nonlocal rules
        nonlocal neighborhood_size

        rules = new_rules
        neighborhood_size = new_neighborhood_size

    initial_grid: Grid = Grid(
        width=5,
        height=5,
        cells=[
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            1,
            1,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
    )

    set_simulation(
        initial_grid=initial_grid,
        generation_count=25,
    )

    app = App(
        get_simulation=get_simulation,
        set_simulation=set_simulation,
        get_rules=get_rules,
        get_neighborhood_size=get_neighborhood_size,
        set_rules=set_rules,
    )

    app.run()


if __name__ == "__main__":
    main()
