class Grid:
    def __init__(self, width: int, height: int, cells: list[int]):
        self.width = width
        self.height = height
        self.cells = cells

    def get_cell(self, x: int, y: int) -> int:
        if len(self.cells) == 0:
            return -1

        x = (x % self.width + self.width) % self.width
        y = (y % self.height + self.height) % self.height

        return self.cells[(self.width * y) + x]
