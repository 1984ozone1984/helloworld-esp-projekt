// Composition root (docs/Method/project/architecture.md). Pipeline skeleton:
// it implements no FSD requirement yet and only proves build -> flash -> observe.
#include "esp_log.h"

static const char *TAG = "main";

void app_main(void)
{
    ESP_LOGI(TAG, "Init complete");
}
