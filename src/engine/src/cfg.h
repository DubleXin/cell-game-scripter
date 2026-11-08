#pragma once
#include "simulation/grid.h"

typedef struct
{
    grid_t *initial_grid;
    long max_sims;
    int width;
    int height;
} cfg_t;

cfg_t *cfg_create(int width, int height, long max_sims);
void cfg_destroy(cfg_t *cfg);