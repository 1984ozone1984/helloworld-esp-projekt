// Composition root (docs/Method/project/architecture.md). Pipeline skeleton:
// it implements no FSD requirement yet and only proves build -> flash -> observe.
// The ON/OFF lines are a periodic marker the bench can match at any moment.
#include <stdbool.h>
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "main";

void app_main(void)
{
    ESP_LOGI(TAG, "Init complete");
    for (bool on = true;; on = !on) {
        ESP_LOGI(TAG, "%s", on ? "ON" : "OFF");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
