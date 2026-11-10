#include <stdio.h>
#include <stdlib.h>

#include "cfg.h"
#include "simulation/grid.h"

int read_grid(cfg_t *cfg, const char *line, int width, int height)
{
    if (!cfg || !cfg->initial_grid || !line ||
        line[0] != '[' || width <= 0 || height <= 0)
    {
        return 1;
    }

    line++;

    int counter = 0;
    int x = 0;
    int y = 0;

    char *end;

    while (*line != ']' && *line != '\0')
    {
        if (counter >= width * height)
        {
            printf(
                "Invalid cell count: %d, expected %d\n",
                counter,
                width * height);

            return 1;
        }

        unsigned long value = strtoul(line, &end, 10);

        if (line == end || (value != 0 && value != 1))
        {
            printf("Invalid cell value: %lu\n", value);
            return 1;
        }

        grid_set_cell(
            cfg->initial_grid,
            (cell_state_t)value,
            x,
            y);

        counter++;

        x++;
        if (x == width)
        {
            x = 0;
            y++;
        }

        line = end;

        if (*line == ']')
            break;

        if (*line != ',')
        {
            printf(
                "Expected ',' or ']', got '%c'\n",
                *line);

            return 1;
        }

        line++;

        if (*line == ']' || *line == '\0')
        {
            printf("Expected cell value after ','\n");
            return 1;
        }
    }

    if (*line != ']')
    {
        printf("Grid is missing closing ']'\n");
        return 1;
    }

    if (counter != width * height)
    {
        printf(
            "Invalid cell count: %d, expected %d\n",
            counter,
            width * height);

        return 1;
    }

    return 0;
}