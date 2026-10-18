// Composition root (docs/Method/project/architecture.md).
#include "blinker.h"
#include "boot_banner.h"
#include "esp_log.h"
#include "fault_inject.h"
#include "heartbeat.h"
#include "led.h"
#include "sdkconfig.h"

static const char *TAG = "main";

void app_main(void)
{
    led_init();
    boot_banner_emit();
#if !CONFIG_HELLO_FAULT_STALL_TASK_NONE
    heartbeat_set_tick_hook(fault_inject_tick);
    blinker_set_tick_hook(fault_inject_tick);
    fault_inject_arm();
#endif
    heartbeat_start();
    blinker_start();
    ESP_LOGI(TAG, "Init complete");
}
