#pragma once

#include "cfg.h"
#include "simulation/grid.h"

cfg_t *read_data(const char *path);

grid_t *read_grid(cfg_t *cfg, const char *line, int width, int height);