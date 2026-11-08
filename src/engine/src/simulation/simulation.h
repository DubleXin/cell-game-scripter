#pragma once

#include "grid.h"
#include <stdbool.h>

typedef struct
{
    grid_t *current_grid;
    long max_sims;
    long current_sim;

} sim_t;

sim_t *sim_create(long max_sims, grid_t *grid);
void sim_destroy(sim_t *sim);

int sim_count_neighbors(grid_t *grid, int x, int y);

cell_state_t sim_get_transition_cell(grid_t *grid, int x, int y);

grid_t *sim_get_next_grid(grid_t *grid);

bool sim_next_gen(sim_t *sim);