#include "reset_reason.h"

// Indexed by esp_reset_reason_t; boot_banner.c pins the values.
static const char *const names[] = {
    "UNKNOWN", "POWERON", "EXT", "SW", "PANIC", "INT_WDT", "TASK_WDT", "WDT",
    "DEEPSLEEP", "BROWNOUT", "SDIO", "USB", "JTAG", "EFUSE", "PWR_GLITCH", "CPU_LOCKUP",
};

const char *reset_reason_name(int reason)
{
    if (reason < 0 || reason >= (int)(sizeof names / sizeof names[0])) {
        return "UNKNOWN";
    }
    return names[reason];
}
