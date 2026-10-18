// Blinker (FSD §7): toggle the LED every 500 ms and log each state.
#pragma once

// The LED driver must be initialised first.
// Optional hook called once per period with the task's name ("blink"), before
// the line is logged. Set before blinker_start(); used only by fault injection.
void blinker_set_tick_hook(void (*hook)(const char *task));
void blinker_start(void);
