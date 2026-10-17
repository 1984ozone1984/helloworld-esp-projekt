// Heartbeat counter (FSD FR-HB-02). Pure: no ESP-IDF includes.
#pragma once
#include <stdint.h>

typedef struct {
    uint32_t n;
} heartbeat_counter_t;

void heartbeat_counter_init(heartbeat_counter_t *c);
// Advance and return the counter for the next heartbeat: 1, 2, 3, ...
uint32_t heartbeat_counter_next(heartbeat_counter_t *c);
