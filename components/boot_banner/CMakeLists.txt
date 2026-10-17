idf_component_register(SRCS "boot_banner.c" "reset_reason.c"
                       INCLUDE_DIRS "include"
                       PRIV_REQUIRES console_fmt esp_app_format)
