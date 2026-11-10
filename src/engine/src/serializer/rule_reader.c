#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

#include "simulation/cell.h"
#include "simulation/rule.h"

static int _parse_rule_values(
    const char *line,
    long *values,
    int max_values,
    int *value_count)
{
    if (!line || !values || !value_count)
        return 1;

    const char *cursor = line;
    int count = 0;

    while (*cursor != '\0' && *cursor != '\n' && *cursor != '\r')
    {
        if (count >= max_values)
            return 1;

        char *end;

        errno = 0;
        long value = strtol(cursor, &end, 10);

        if (cursor == end || errno == ERANGE)
            return 1;

        values[count++] = value;
        cursor = end;

        if (*cursor == '_')
        {
            cursor++;

            if (*cursor == '\0' || *cursor == '\n' || *cursor == '\r')
                return 1;

            continue;
        }

        if (*cursor == '\r')
            cursor++;

        if (*cursor != '\n' && *cursor != '\0')
            return 1;
    }

    *value_count = count;

    return count == 0;
}

int read_rule(rule_t *rule, const char *line, int neighborhood_size)
{
    if (!rule || !line || neighborhood_size <= 0)
        return 1;

    long values[7];
    int value_count = 0;

    if (_parse_rule_values(line, values, 7, &value_count) != 0)
    {
        printf("Invalid rule format: %s", line);
        return 1;
    }

    if (value_count < 2)
    {
        printf("Incomplete rule: %s", line);
        return 1;
    }

    long target_state = values[0];
    long rule_type = values[1];

    if (target_state != DEAD && target_state != ALIVE)
    {
        printf("Invalid target state: %ld\n", target_state);
        return 1;
    }

    if (rule_type == RULE_POPULATION)
    {
        if (value_count != 5)
        {
            printf("Population rule requires 5 values\n");
            return 1;
        }

        long comparison = values[2];
        long value = values[3];
        long result = values[4];

        if (comparison < RULE_EQUAL || comparison > RULE_LESS)
        {
            printf("Invalid comparison: %ld\n", comparison);
            return 1;
        }

        int max_population = neighborhood_size * neighborhood_size - 1;

        if (value < 0 || value > max_population)
        {
            printf("Invalid population value: %ld\n", value);
            return 1;
        }

        if (result != DEAD && result != ALIVE)
        {
            printf("Invalid result state: %ld\n", result);
            return 1;
        }

        rule->target_state = (cell_state_t)target_state;
        rule->type = RULE_POPULATION;
        rule->comparison = (rule_comparison_t)comparison;
        rule->result = (cell_state_t)result;
        rule->args[0] = (int)value;
        rule->args[1] = 0;

        return 0;
    }

    if (rule_type == RULE_NEIGHBOR)
    {
        if (value_count != 7)
        {
            printf("Neighbor rule requires 7 values\n");
            return 1;
        }

        long x = values[2];
        long y = values[3];
        long comparison = values[4];
        long value = values[5];
        long result = values[6];

        if (x < 0 || x >= neighborhood_size ||
            y < 0 || y >= neighborhood_size)
        {
            printf("Invalid neighbor position: %ld_%ld\n", x, y);
            return 1;
        }

        int center = neighborhood_size / 2;

        if (x == center && y == center)
        {
            printf("Neighbor cannot be target cell\n");
            return 1;
        }

        if (comparison < RULE_EQUAL || comparison > RULE_LESS)
        {
            printf("Invalid comparison: %ld\n", comparison);
            return 1;
        }

        if (value != DEAD && value != ALIVE)
        {
            printf("Invalid neighbor state: %ld\n", value);
            return 1;
        }

        if (result != DEAD && result != ALIVE)
        {
            printf("Invalid result state: %ld\n", result);
            return 1;
        }

        rule->target_state = (cell_state_t)target_state;
        rule->type = RULE_NEIGHBOR;
        rule->comparison = (rule_comparison_t)comparison;
        rule->result = (cell_state_t)result;

        //  Flatten x_y into one value.
        rule->args[0] = (int)y * neighborhood_size + (int)x;
        rule->args[1] = (int)value;

        return 0;
    }

    printf("Invalid rule type: %ld\n", rule_type);

    return 1;
}