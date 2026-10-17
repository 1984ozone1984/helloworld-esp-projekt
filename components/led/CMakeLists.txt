idf_component_register(SRCS "led.c" "led_core.c"
                       INCLUDE_DIRS "include"
                       PRIV_REQUIRES esp_driver_gpio)
