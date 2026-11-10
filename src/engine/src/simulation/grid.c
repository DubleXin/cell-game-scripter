#include "simulation/grid.h"

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

grid_t *grid_create(int width, int height)
{
    if (width < 0 || height < 0)
        return NULL;

    grid_t *new_grid = malloc(sizeof(grid_t));
    if (!new_grid)
        return NULL;

    new_grid->cells = calloc((width * height), sizeof(uint8_t));
    new_grid->width = width;
    new_grid->height = height;

    if (!new_grid->cells)
    {
        free(new_grid);
        return NULL;
    }

    return new_grid;
}

grid_t *grid_clone(grid_t *grid)
{
    grid_t *new = grid_create(grid->width, grid->height);
    for (int i = 0; i < grid->width; i++)
    {
        for (int j = 0; j < grid->height; j++)
        {
            grid_set_cell(new, grid_get_cell(grid, i, j), i, j);
        }
    }
    return new;
}

void grid_destroy(grid_t *grid)
{
    free(grid->cells);
    free(grid);
}

int grid_get_index(const grid_t *grid, int x, int y)
{
    x = (x % grid->width + grid->width) % grid->width;
    y = (y % grid->height + grid->height) % grid->height;
    return (grid->width * y) + x;
}

void grid_set_cell(grid_t *grid, cell_state_t state, int x, int y)
{
    grid->cells[grid_get_index(grid, x, y)] = (uint8_t)state;
}

cell_state_t grid_get_cell(const grid_t *grid, int x, int y)
{
    return (cell_state_t)grid->cells[grid_get_index(grid, x, y)];
}

void grid_print(grid_t *grid)
{
    printf("\n\n");

    for (int i = 0; i < grid->width; i++)
    {
        for (int j = 0; j < grid->height; j++)
        {
            const char *ch = grid_get_cell(grid, i, j) == ALIVE ? "█" : "░";
            printf("%s", ch);
        }
        printf("\n");
    }

    printf("\n\n");
}