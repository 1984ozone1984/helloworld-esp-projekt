// Composition root (docs/Method/project/architecture.md).
#include "blinker.h"
#include "boot_banner.h"
#include "esp_log.h"
#include "heartbeat.h"
#include "led.h"

static const char *TAG = "main";

void app_main(void)
{
    led_init();
    boot_banner_emit();
    heartbeat_start();
    blinker_start();
    ESP_LOGI(TAG, "Init complete");
}
