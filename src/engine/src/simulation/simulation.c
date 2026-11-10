#include "simulation.h"

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "simulation/cell.h"
#include "simulation/grid.h"
#include "simulation/rule.h"

static bool _compare(int left, rule_comparison_t comparison, int right)
{
    switch (comparison)
    {
    case RULE_EQUAL:
        return left == right;

    case RULE_GREATER:
        return left > right;

    case RULE_LESS:
        return left < right;
    }

    return false;
}

static cell_state_t _apply_rules(const sim_t *sim, grid_t *grid, int x, int y)
{
    cell_state_t current_state = grid_get_cell(grid, x, y);

    for (int i = 0; i < sim->rule_count; i++)
    {
        const rule_t *rule =
            &sim->rules[i];

        if (rule->target_state != current_state)
            continue;

        bool matched = false;

        if (rule->type == RULE_POPULATION)
        {
            int population = sim_count_neighbors(grid, x, y, sim->neighborhood_size);

            matched = _compare(
                population,
                rule->comparison,
                rule->args[0]);
        }
        else if (rule->type == RULE_NEIGHBOR)
        {
            /*
             * args[0] contains flattened
             * neighborhood position.
             *
             * Example for 3x3:
             *
             * 0 1 2
             * 3 4 5
             * 6 7 8
             */
            int neighbor_index = rule->args[0];

            int local_x = neighbor_index % sim->neighborhood_size;
            int local_y = neighbor_index / sim->neighborhood_size;

            int center = sim->neighborhood_size / 2;

            int offset_x = local_x - center;
            int offset_y = local_y - center;

            cell_state_t neighbor_state = grid_get_cell(grid, x + offset_x, y + offset_y);

            matched = _compare(
                (int)neighbor_state,
                rule->comparison,
                rule->args[1]);
        }

        if (matched)
            return rule->result;
    }
    return current_state;
}

sim_t *sim_create(
    long max_sims,
    grid_t *grid,
    const rule_t *rules,
    int rule_count,
    int neighborhood_size)
{
    if (!grid ||
        max_sims <= 0 ||
        rule_count < 0 ||
        neighborhood_size < 3 ||
        neighborhood_size % 2 == 0)
    {
        return NULL;
    }

    if (rule_count > 0 && !rules)
        return NULL;

    sim_t *new_sim = malloc(sizeof(sim_t));

    if (!new_sim)
        return NULL;

    new_sim->current_grid = grid_clone(grid);

    if (!new_sim->current_grid)
    {
        free(new_sim);
        return NULL;
    }

    new_sim->rules = NULL;
    new_sim->rule_count = rule_count;

    if (rule_count > 0)
    {
        new_sim->rules = malloc(sizeof(rule_t) * (size_t)rule_count);

        if (!new_sim->rules)
        {
            grid_destroy(new_sim->current_grid);
            free(new_sim);

            return NULL;
        }

        memcpy(new_sim->rules, rules, sizeof(rule_t) * (size_t)rule_count);
    }

    new_sim->max_sims = max_sims;
    new_sim->current_sim = 0;
    new_sim->neighborhood_size = neighborhood_size;

    return new_sim;
}

void sim_destroy(sim_t *sim)
{
    if (!sim)
        return;

    if (sim->current_grid)
        grid_destroy(sim->current_grid);

    free(sim->rules);
    free(sim);
}

int sim_count_neighbors(grid_t *grid, int x, int y, int neighborhood_size)
{
    int count = 0;

    int center = neighborhood_size / 2;
    int top_left_x = x - center;
    int top_left_y = y - center;

    for (int local_y = 0; local_y < neighborhood_size; local_y++)
    {
        for (int local_x = 0; local_x < neighborhood_size; local_x++)
        {
            if (local_x == center && local_y == center)
                continue;

            if (grid_get_cell(grid, top_left_x + local_x, top_left_y + local_y) == ALIVE)
            {
                count++;
            }
        }
    }

    return count;
}

grid_t *sim_get_next_grid(sim_t *sim)
{
    if (!sim || !sim->current_grid)
        return NULL;

    grid_t *grid = sim->current_grid;
    grid_t *new_grid = grid_create(grid->width, grid->height);

    if (!new_grid)
        return NULL;

    for (int y = 0; y < grid->height; y++)
    {
        for (int x = 0; x < grid->width; x++)
        {
            cell_state_t new_state = _apply_rules(sim, grid, x, y);
            grid_set_cell(new_grid, new_state, x, y);
        }
    }

    return new_grid;
}

bool sim_next_gen(sim_t *sim)
{
    if (!sim)
        return false;

    if (sim->current_sim > sim->max_sims)
        return false;

    grid_t *next = sim_get_next_grid(sim);

    if (!next)
        return false;

    grid_t *old = sim->current_grid;

    sim->current_grid = next;

    grid_destroy(old);

    return true;
}