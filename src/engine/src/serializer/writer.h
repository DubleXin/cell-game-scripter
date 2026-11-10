#pragma once
#include "simulation/grid.h"

int write_gen_line(const char *path, long current_gen, grid_t *grid);
int write_headers(const char *path, int width, int height, long max_sims);