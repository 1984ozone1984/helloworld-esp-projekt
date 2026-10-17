#include "heartbeat_core.h"

void heartbeat_counter_init(heartbeat_counter_t *c)
{
    c->n = 0;
}

uint32_t heartbeat_counter_next(heartbeat_counter_t *c)
{
    return ++c->n;
}
