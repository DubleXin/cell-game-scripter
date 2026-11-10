#include <stdio.h>
#include "cfg.h"
#include "runner/runner.h"
#include "simulation/grid.h"
#include "simulation/simulation.h"
#include "serializer/writer.h"

int run(cfg_t *cfg)
{
    if (!cfg || cfg->width == 0 || cfg->height == 0 || cfg->max_sims == 0 || !cfg->initial_grid)
        return 1;

    sim_t *sim = sim_create(
        cfg->max_sims,
        cfg->initial_grid,
        cfg->rules,
        cfg->rule_count,
        cfg->neighborhood_size);

    if (!sim)
        return 1;

    do
    {
        // printf("%ld\n", sim->current_sim);
        // grid_print(sim->current_grid);`'
        if (!write_gen_line(NULL, sim->current_sim++, sim->current_grid))
        {
            printf("Failed to write gen: %ld", sim->current_sim - 1);
            sim_destroy(sim);
            return 1;
        }

    } while (sim_next_gen(sim));

    sim_destroy(sim);

    return 0;
}