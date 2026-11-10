#include "cfg.h"

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include "serializer/reader.h"

static int _parse_grid_line(const char *line, long *result)
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

cfg_t *read_data(const char *init_grid_path, const char *rules_path)
{
    if (!init_grid_path)
        init_grid_path = ".data/.input_grid";

    if (!rules_path)
        rules_path = ".data/.rules";

    FILE *grid_fptr = fopen(init_grid_path, "r");

    if (!grid_fptr)
    {
        printf("Failed to open file: %s\n", init_grid_path);
        return NULL;
    }

    char current_line[100];

    long width_value;
    long height_value;
    long max_sims;

    // Width
    if (!fgets(current_line, sizeof(current_line), grid_fptr) ||
        _parse_grid_line(current_line, &width_value) != 0 ||
        width_value < 3 ||
        width_value > 100)
    {
        printf("Invalid width\n");
        fclose(grid_fptr);
        return NULL;
    }

    // Height
    if (!fgets(current_line, sizeof(current_line), grid_fptr) ||
        _parse_grid_line(current_line, &height_value) != 0 ||
        height_value < 3 ||
        height_value > 100)
    {
        printf("Invalid height\n");
        fclose(grid_fptr);
        return NULL;
    }

    // Max simulations
    if (!fgets(current_line, sizeof(current_line), grid_fptr) ||
        _parse_grid_line(current_line, &max_sims) != 0 ||
        max_sims <= 0)
    {
        printf("Invalid max_sims\n");
        fclose(grid_fptr);
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
        fclose(grid_fptr);
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
        fclose(grid_fptr);
        return NULL;
    }

    if (!fgets(
            grid_line,
            (int)grid_line_size,
            grid_fptr))
    {
        printf("Failed to read grid\n");

        free(grid_line);
        cfg_destroy(cfg);
        fclose(grid_fptr);

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
        fclose(grid_fptr);

        return NULL;
    }

    free(grid_line);
    fclose(grid_fptr);

    FILE *rules_fptr = fopen(rules_path, "r");

    if (!rules_fptr)
    {
        printf("Failed to open file: %s\n", rules_path);
        cfg_destroy(cfg);
        return NULL;
    }

    long neighborhood_size_value;
    long rule_count_value;

    /* Neighborhood size */
    if (!fgets(
            current_line,
            sizeof(current_line),
            rules_fptr) ||
        _parse_grid_line(
            current_line,
            &neighborhood_size_value) != 0 ||
        neighborhood_size_value < 3 ||
        neighborhood_size_value > 9 ||
        neighborhood_size_value % 2 == 0)
    {
        printf("Invalid neighborhood size\n");

        fclose(rules_fptr);
        cfg_destroy(cfg);

        return NULL;
    }

    /* Rule count */
    if (!fgets(
            current_line,
            sizeof(current_line),
            rules_fptr) ||
        _parse_grid_line(
            current_line,
            &rule_count_value) != 0 ||
        rule_count_value < 0 ||
        rule_count_value > INT_MAX)
    {
        printf("Invalid rule count\n");

        fclose(rules_fptr);
        cfg_destroy(cfg);

        return NULL;
    }

    cfg->neighborhood_size = (int)neighborhood_size_value;
    cfg->rule_count = (int)rule_count_value;

    if (cfg->rule_count > 0)
    {
        cfg->rules = calloc((size_t)cfg->rule_count, sizeof(rule_t));

        if (!cfg->rules)
        {
            printf("Failed to allocate rules\n");

            fclose(rules_fptr);
            cfg_destroy(cfg);

            return NULL;
        }
    }

    int rules_read = 0;

    while (rules_read < cfg->rule_count)
    {
        if (!fgets(
                current_line,
                sizeof(current_line),
                rules_fptr))
        {
            printf(
                "Rule count mismatch: "
                "expected %d, got %d\n",
                cfg->rule_count,
                rules_read);

            fclose(rules_fptr);
            cfg_destroy(cfg);

            return NULL;
        }

        if (read_rule(
                &cfg->rules[rules_read],
                current_line,
                cfg->neighborhood_size) != 0)
        {
            printf("Failed to parse rule %d\n", rules_read);

            fclose(rules_fptr);
            cfg_destroy(cfg);

            return NULL;
        }

        rules_read++;
    }

    if (fgets(
            current_line,
            sizeof(current_line),
            rules_fptr))
    {
        printf(
            "Rule count mismatch: "
            "expected %d, file contains more rules\n",
            cfg->rule_count);

        fclose(rules_fptr);
        cfg_destroy(cfg);

        return NULL;
    }

    if (rules_read != cfg->rule_count)
    {
        printf(
            "Rule count mismatch: "
            "expected %d, got %d\n",
            cfg->rule_count,
            rules_read);

        fclose(rules_fptr);
        cfg_destroy(cfg);

        return NULL;
    }

    fclose(rules_fptr);

    return cfg;
}