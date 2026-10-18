#include "fault_inject.h"

#include <stdint.h>
#include <string.h>

#include "console_fmt.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"

#define FAULT_AFTER_US (10 * 1000 * 1000)

static int64_t s_armed_us = -1;

void fault_inject_arm(void)
{
    s_armed_us = esp_timer_get_time();
}

void fault_inject_tick(const char *task)
{
    if (s_armed_us < 0 || strcmp(task, CONFIG_HELLO_FAULT_STALL_TASK) != 0
        || esp_timer_get_time() - s_armed_us < FAULT_AFTER_US) {
        return;
    }
    char line[32];
    if (fmt_fault(line, sizeof line, task) >= 0) {
        ESP_LOGW(CONSOLE_TAG_FAULT, "%s", line);
    }
    // Never resets the TWDT again: the watchdog must fire (FR-WDT-01).
    for (;;) {
        vTaskDelay(portMAX_DELAY);
    }
}
