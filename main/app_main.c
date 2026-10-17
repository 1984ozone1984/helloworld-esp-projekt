// Composition root (docs/Method/project/architecture.md).
#include <stdbool.h>
#include "boot_banner.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "main";

void app_main(void)
{
    boot_banner_emit();
    ESP_LOGI(TAG, "Init complete");
    // Pipeline marker until the heartbeat and blinker land (FSD §6, §7).
    for (bool on = true;; on = !on) {
        ESP_LOGI(TAG, "%s", on ? "ON" : "OFF");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
