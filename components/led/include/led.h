// LED driver (FSD §9): the onboard user LED on GPIO21 (CON-05).
#pragma once
#include <stdbool.h>

// Configure GPIO21 as a push-pull output, LED dark.
void led_init(void);
void led_set(bool on);
