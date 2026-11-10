#pragma once
#include "simulation/grid.h"
#include "simulation/rule.h"

typedef struct
{
    grid_t *initial_grid;
    rule_t *rules;

    long max_sims;

    int width;
    int height;

    int neighborhood_size;
    int rule_count;
} cfg_t;

cfg_t *cfg_create(int width, int height, long max_sims);
void cfg_destroy(cfg_t *cfg);