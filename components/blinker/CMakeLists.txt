idf_component_register(SRCS "blinker.c" "blink_core.c"
                       INCLUDE_DIRS "include"
                       PRIV_REQUIRES console_fmt led esp_system)
