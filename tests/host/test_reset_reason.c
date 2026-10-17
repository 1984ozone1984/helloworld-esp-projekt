// TC-BOOT-03-host — FSD FR-BOOT-03 (a): every reset reason maps to its A.2 name;
// out-of-range values map to UNKNOWN. Values are esp_reset_reason_t's, which
// boot_banner.c pins with static asserts.
#include "check.h"
#include "reset_reason.h"

int main(void)
{
    const char *want[] = {"UNKNOWN", "POWERON", "EXT", "SW", "PANIC", "INT_WDT",
                          "TASK_WDT", "WDT", "DEEPSLEEP", "BROWNOUT", "SDIO", "USB",
                          "JTAG", "EFUSE", "PWR_GLITCH", "CPU_LOCKUP"};
    for (int v = 0; v < 16; v++) {
        CHECK_STR(reset_reason_name(v), want[v]);
    }
    CHECK_STR(reset_reason_name(16), "UNKNOWN");
    CHECK_STR(reset_reason_name(99), "UNKNOWN");
    CHECK_STR(reset_reason_name(-1), "UNKNOWN");
    return CHECK_DONE();
}
