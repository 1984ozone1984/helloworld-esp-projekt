// Fault injection (FSD §11): stall one task 10 s after RUNNING. Fault variants only.
#pragma once

// Start the 10 s clock; call once, when RUNNING begins.
void fault_inject_arm(void);
// Tick hook for a task loop: blocks the configured task forever once due.
void fault_inject_tick(const char *task);
