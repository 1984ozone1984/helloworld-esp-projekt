idf_component_register(SRCS "heartbeat.c" "heartbeat_core.c"
                       INCLUDE_DIRS "include"
                       PRIV_REQUIRES console_fmt esp_timer esp_system)
