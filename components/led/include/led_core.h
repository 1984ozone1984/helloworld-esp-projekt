// LED pin level (FSD CON-05): the user LED is active-low. Pure.
#pragma once
#include <stdbool.h>

// GPIO level that puts the LED in `on`: 0 lights it, 1 darkens it.
int led_level(bool on);
