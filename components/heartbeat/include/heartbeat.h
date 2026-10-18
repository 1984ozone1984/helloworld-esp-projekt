// Heartbeat (FSD §6): one line every 1000 ms while RUNNING.
#pragma once

// Optional hook called once per period with the task's name ("heartbeat"), before
// the line is logged. Set before heartbeat_start(); used only by fault injection.
void heartbeat_set_tick_hook(void (*hook)(const char *task));
void heartbeat_start(void);
