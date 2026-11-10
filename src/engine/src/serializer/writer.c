#include <stdio.h>

#include "simulation/grid.h"
#include "serializer/writer.h"

int write_headers(const char *path, int width, int height, long max_sims)
{
    if (!path)
        path = ".data/.output";

    FILE *fptr = fopen(path, "w");

    if (!fptr)
    {
        printf("Failed to open file: %s\n", path);
        return 0;
    }

    fprintf(fptr, "%d\n", width);
    fprintf(fptr, "%d\n", height);
    fprintf(fptr, "%ld\n", max_sims);

    fclose(fptr);

    return 1;
}

int write_gen_line(const char *path, long current_gen, grid_t *grid)
{
    if (!grid)
        return 0;

    if (!path)
        path = ".data/.output";

    FILE *fptr = fopen(path, "a");

    if (!fptr)
    {
        printf("Failed to open file: %s\n", path);
        return 0;
    }

    int cell_count = grid->width * grid->height;
    char data[3 * cell_count + 2];

    int pos = 0;

    data[pos++] = '[';

    for (int i = 0; i < cell_count; i++)
    {
        data[pos++] = '0' + grid->cells[i];

        if (i < cell_count - 1)
        {
            data[pos++] = ',';
            data[pos++] = ' ';
        }
    }

    data[pos++] = ']';
    data[pos++] = '\n';
    data[pos] = '\0';

    fprintf(fptr, "%ld\n", current_gen);
    fprintf(fptr, "%s", data);

    fclose(fptr);

    return 1;
}