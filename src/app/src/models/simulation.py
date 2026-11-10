from app.src.models.grid import Grid


class Simulation:
    def __init__(self, snapshots: list[Grid]):
        self.snapshots = snapshots

    def __len__(self) -> int:
        return len(self.snapshots)

    def __getitem__(self, index: int) -> Grid:
        return self.snapshots[index]

    def __iter__(self):
        return iter(self.snapshots)

    def __contains__(self, item: Grid) -> bool:
        return item in self.snapshots
