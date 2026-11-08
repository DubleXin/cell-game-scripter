from app.src.models.simulation import Simulation


def print_sim(simulation: Simulation) -> None:
    for generation, grid in enumerate(simulation):
        print(f"\nGeneration {generation}\n")

        for y in range(grid.height):
            for x in range(grid.width):
                index: int = y * grid.width + x
                char: str = "█" if grid.cells[index] == 1 else "░"

                print(char, end="")

            print()

        print()
