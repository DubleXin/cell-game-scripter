import tkinter as tk

from app.src.models.grid import Grid


def render_grid(
    canvas: tk.Canvas,
    grid: Grid,
) -> None:
    canvas.delete("all")

    canvas_width: int = canvas.winfo_width()
    canvas_height: int = canvas.winfo_height()

    cell_width: float = canvas_width / grid.width
    cell_height: float = canvas_height / grid.height

    for y in range(grid.height):
        for x in range(grid.width):
            index: int = y * grid.width + x

            x1: float = x * cell_width
            y1: float = y * cell_height
            x2: float = x1 + cell_width
            y2: float = y1 + cell_height

            fill: str = "black" if grid.cells[index] == 1 else "white"

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=fill,
                outline="gray",
            )
