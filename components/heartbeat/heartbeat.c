#include "heartbeat.h"

#include "console_fmt.h"
#include "esp_log.h"
#include "esp_task_wdt.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "heartbeat_core.h"

#define HEARTBEAT_PERIOD_MS 1000

static void heartbeat_task(void *arg)
{
    (void)arg;
    ESP_ERROR_CHECK(esp_task_wdt_add(NULL));
    heartbeat_counter_t counter;
    heartbeat_counter_init(&counter);
    char line[64];
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        vTaskDelayUntil(&wake, pdMS_TO_TICKS(HEARTBEAT_PERIOD_MS));
        ESP_ERROR_CHECK(esp_task_wdt_reset());
        uint32_t uptime_ms = (uint32_t)(esp_timer_get_time() / 1000);
        if (fmt_heartbeat(line, sizeof line, heartbeat_counter_next(&counter), uptime_ms) >= 0) {
            ESP_LOGI(CONSOLE_TAG_HELLO, "%s", line);
        }
    }
}

void heartbeat_start(void)
{
    if (xTaskCreate(heartbeat_task, "heartbeat", 3072, NULL, 5, NULL) != pdPASS) {
        ESP_ERROR_CHECK(ESP_ERR_NO_MEM);
    }
}
