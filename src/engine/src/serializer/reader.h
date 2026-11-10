#pragma once

#include "cfg.h"

cfg_t *read_data(const char *init_grid_path, const char *rules_path);

int read_grid(cfg_t *cfg, const char *line, int width, int height);

int read_rule(rule_t *rule, const char *line, int neighborhood_size);