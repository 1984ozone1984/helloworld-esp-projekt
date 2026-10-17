#include "boot_banner.h"

#include "console_fmt.h"
#include "esp_app_desc.h"
#include "esp_log.h"
#include "esp_system.h"
#include "reset_reason.h"

// reset_reason_name() indexes by these values; fail the build if IDF renumbers.
_Static_assert(ESP_RST_UNKNOWN == 0, "reset reason table");
_Static_assert(ESP_RST_POWERON == 1, "reset reason table");
_Static_assert(ESP_RST_PANIC == 4, "reset reason table");
_Static_assert(ESP_RST_TASK_WDT == 6, "reset reason table");
_Static_assert(ESP_RST_USB == 11, "reset reason table");
_Static_assert(ESP_RST_JTAG == 12, "reset reason table");
_Static_assert(ESP_RST_CPU_LOCKUP == 15, "reset reason table");

void boot_banner_emit(void)
{
    char line[160];
    if (fmt_banner(line, sizeof line, esp_app_get_description()->version,
                   reset_reason_name(esp_reset_reason())) < 0) {
        ESP_LOGE(CONSOLE_TAG_HELLO, "banner does not fit");
        return;
    }
    ESP_LOGI(CONSOLE_TAG_HELLO, "%s", line);
}
