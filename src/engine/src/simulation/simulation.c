#include "simulation.h"
#include <stdlib.h>
#include <simulation/cell.h>
#include <simulation/grid.h>
#include <stdbool.h>
#include <stdio.h>

sim_t *sim_create(long max_sims, grid_t *grid)
{
    if (!grid)
        return NULL;

    sim_t *new_sim = malloc(sizeof(sim_t));
    if (!new_sim)
        return NULL;

    new_sim->current_grid = grid_clone(grid);
    new_sim->max_sims = max_sims;
    new_sim->current_sim = 0;

    return new_sim;
}

void sim_destroy(sim_t *sim)
{
    if (sim->current_grid)
        grid_destroy(sim->current_grid);
    free(sim);
}

int sim_count_neighbors(grid_t *grid, int x, int y)
{
    // TODO: get size from cfg
    const int N = 3;
    int count = 0;

    int top_left_x = x - ((N - 1) / 2);
    int top_left_y = y - ((N - 1) / 2);
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            if (top_left_x + i == x && top_left_y + j == y)
                continue;
            if (grid_get_cell(grid, top_left_x + i, top_left_y + j) == ALIVE)
                count++;
        }
    }

    return count;
}

cell_state_t sim_get_transition_cell(grid_t *grid, int x, int y)
{
    // TODO: it's a place where custom rules should live
    int alive_neighbors = sim_count_neighbors(grid, x, y);
    cell_state_t state = grid_get_cell(grid, x, y);
    if (state == ALIVE && (alive_neighbors < 2 || alive_neighbors > 3))
        return DEAD;
    if (state == DEAD && alive_neighbors == 3)
        return ALIVE;
    return state;
}

grid_t *sim_get_next_grid(grid_t *grid)
{
    grid_t *new_grid = grid_create(grid->width, grid->height);

    for (int i = 0; i < grid->width; i++)
        for (int j = 0; j < grid->height; j++)
            grid_set_cell(new_grid, sim_get_transition_cell(grid, i, j), i, j);

    return new_grid;
}

bool sim_next_gen(sim_t *sim)
{
    if (sim->current_sim > sim->max_sims)
        return false;

    grid_t *old = sim->current_grid;
    sim->current_grid = sim_get_next_grid(sim->current_grid);
    grid_destroy(old);
    return true;
}