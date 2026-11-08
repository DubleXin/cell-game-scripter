#include "cfg.h"
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

#include "simulation/cell.h"
#include "simulation/grid.h"

static int _parse_long_line(const char *line, long *result)
{
    if (!line || !result)
        return 1;

    char *end;

    errno = 0;
    long value = strtol(line, &end, 10);

    // No number was parsed or the value overflowed long.
    if (line == end || errno == ERANGE)
        return 1;

    // Allow whitespace after the number.
    while (*end == ' ' || *end == '\t' || *end == '\r')
        end++;

    // fgets() usually leaves '\n' in the buffer.
    if (*end != '\n' && *end != '\0')
        return 1;

    *result = value;
    return 0;
}

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

cfg_t *read_data(const char *path)
{
    if (!path)
        path = ".data/.input";

    FILE *fptr = fopen(path, "r");

    if (!fptr)
    {
        printf("Failed to open file: %s\n", path);
        return NULL;
    }

    char current_line[1000];

    long width_value;
    long height_value;
    long max_sims;

    // Width
    if (!fgets(current_line, sizeof(current_line), fptr) ||
        _parse_long_line(current_line, &width_value) != 0 ||
        width_value < 3 ||
        width_value > 100)
    {
        printf("Invalid width\n");
        fclose(fptr);
        return NULL;
    }

    // Height
    if (!fgets(current_line, sizeof(current_line), fptr) ||
        _parse_long_line(current_line, &height_value) != 0 ||
        height_value < 3 ||
        height_value > 100)
    {
        printf("Invalid height\n");
        fclose(fptr);
        return NULL;
    }

    // Max simulations
    if (!fgets(current_line, sizeof(current_line), fptr) ||
        _parse_long_line(current_line, &max_sims) != 0 ||
        max_sims <= 0)
    {
        printf("Invalid max_sims\n");
        fclose(fptr);
        return NULL;
    }

    int width = (int)width_value;
    int height = (int)height_value;

    cfg_t *cfg = cfg_create(
        width,
        height,
        max_sims);

    if (!cfg)
    {
        fclose(fptr);
        return NULL;
    }

    size_t cell_count =
        (size_t)width * (size_t)height;

    size_t grid_line_size =
        3 * cell_count + 2;

    char *grid_line = malloc(
        grid_line_size);

    if (!grid_line)
    {
        printf("Failed to allocate grid buffer\n");
        cfg_destroy(cfg);
        fclose(fptr);
        return NULL;
    }

    if (!fgets(
            grid_line,
            (int)grid_line_size,
            fptr))
    {
        printf("Failed to read grid\n");

        free(grid_line);
        cfg_destroy(cfg);
        fclose(fptr);

        return NULL;
    }

    if (read_grid(
            cfg,
            grid_line,
            width,
            height) != 0)
    {
        free(grid_line);
        cfg_destroy(cfg);
        fclose(fptr);

        return NULL;
    }

    free(grid_line);
    fclose(fptr);

    return cfg;
}