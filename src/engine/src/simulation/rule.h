#pragma once
#include "simulation/cell.h"

typedef enum
{
    RULE_POPULATION = 0,
    RULE_NEIGHBOR = 1
} rule_type_t;

typedef enum
{
    RULE_EQUAL = 0,
    RULE_GREATER = 1,
    RULE_LESS = 2
} rule_comparison_t;

typedef struct
{
    cell_state_t target_state;

    rule_type_t type;
    rule_comparison_t comparison;

    cell_state_t result;

    int args[2];
} rule_t;