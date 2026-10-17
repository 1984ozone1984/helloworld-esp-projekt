#include "led.h"

#include "driver/gpio.h"
#include "esp_err.h"
#include "led_core.h"

#define LED_GPIO GPIO_NUM_21

void led_init(void)
{
    // Level first, so the pad never drives the LED on while becoming an output.
    ESP_ERROR_CHECK(gpio_set_level(LED_GPIO, led_level(false)));
    const gpio_config_t cfg = {
        .pin_bit_mask = 1ULL << LED_GPIO,
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    ESP_ERROR_CHECK(gpio_config(&cfg));
    ESP_ERROR_CHECK(gpio_set_level(LED_GPIO, led_level(false)));
}

void led_set(bool on)
{
    ESP_ERROR_CHECK(gpio_set_level(LED_GPIO, led_level(on)));
}
