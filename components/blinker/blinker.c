#include "blinker.h"

#include "blink_core.h"
#include "console_fmt.h"
#include "esp_log.h"
#include "esp_task_wdt.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "led.h"

#define BLINK_HALF_PERIOD_MS 500

static void blink_task(void *arg)
{
    (void)arg;
    ESP_ERROR_CHECK(esp_task_wdt_add(NULL));
    bool on = false;
    char line[16];
    TickType_t wake = xTaskGetTickCount();
    for (;;) {
        vTaskDelayUntil(&wake, pdMS_TO_TICKS(BLINK_HALF_PERIOD_MS));
        ESP_ERROR_CHECK(esp_task_wdt_reset());
        on = blink_toggle(on);
        led_set(on);
        if (fmt_led(line, sizeof line, on) >= 0) {
            ESP_LOGI(CONSOLE_TAG_LED, "%s", line);
        }
    }
}

void blinker_start(void)
{
    if (xTaskCreate(blink_task, "blink", 3072, NULL, 5, NULL) != pdPASS) {
        ESP_ERROR_CHECK(ESP_ERR_NO_MEM);
    }
}
