#include "cfg.h"
#include <stdlib.h>
#include "simulation/grid.h"
#include <stdio.h>

cfg_t *cfg_create(int width, int height, long max_sims)
{
    cfg_t *cfg = malloc(sizeof(cfg_t));
    if (!cfg)
        return NULL;

    cfg->height = height;
    cfg->width = width;

    cfg->initial_grid = grid_create(width, height);

    if (!cfg->initial_grid)
    {
        free(cfg);
        return NULL;
    }
    cfg->max_sims = max_sims;

    cfg->neighborhood_size = 0;
    cfg->rules = NULL;
    cfg->rule_count = 0;

    return cfg;
}

void cfg_destroy(cfg_t *cfg)
{
    if (cfg->initial_grid)
        grid_destroy(cfg->initial_grid);
    if (cfg->rules)
        free(cfg->rules);
    free(cfg);
}