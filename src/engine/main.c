#include <stdio.h>
#include "cfg.h"
#include "serializer/reader.h"
#include "runner/runner.h"
#include "serializer/writer.h"

int main()
{
    cfg_t *cfg = read_data(NULL);
    if (!cfg)
        return 1;

    printf("Read config file:\nwidth: %d\theight: %d\tmaximum simulations: %ld\n", cfg->width, cfg->height, cfg->max_sims);

    if (!write_headers(NULL, cfg->width, cfg->height, cfg->max_sims))
    {
        printf("Failed to write headers...\n");
        return 1;
    }
    int status = run(cfg);

    cfg_destroy(cfg);

    return status;
}