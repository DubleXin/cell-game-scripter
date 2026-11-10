#pragma once

#include "grid.h"
#include <stdbool.h>

#include "simulation/rule.h"
typedef struct
{
    grid_t *current_grid;
    rule_t *rules;

    long max_sims;
    long current_sim;

    int neighborhood_size;
    int rule_count;

} sim_t;

sim_t *sim_create(long max_sims, grid_t *grid, const rule_t *rules, int rule_count, int neighborhood_size);
void sim_destroy(sim_t *sim);

int sim_count_neighbors(grid_t *grid, int x, int y, int neighborhood_size);

cell_state_t sim_get_transition_cell(grid_t *grid, int x, int y);

grid_t *sim_get_next_grid(sim_t *sim);

bool sim_next_gen(sim_t *sim);