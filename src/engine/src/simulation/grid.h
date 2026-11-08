#pragma once

#include <stdint.h>
#include "simulation/cell.h"

typedef struct
{
    int width;
    int height;
    uint8_t *cells;
} grid_t;

grid_t *grid_create(int width, int height);
void grid_destroy(grid_t *grid);

grid_t *grid_clone(grid_t *grid);

int grid_get_index(const grid_t *grid, int x, int y);

void grid_set_cell(grid_t *grid, cell_state_t state, int x, int y);
cell_state_t grid_get_cell(const grid_t *grid, int x, int y);

void grid_print(grid_t *grid);