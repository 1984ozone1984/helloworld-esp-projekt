# Compiled in only for a fault variant; a release image links an empty component.
set(srcs)
if(CONFIG_HELLO_FAULT_STALL_TASK_BLINK OR CONFIG_HELLO_FAULT_STALL_TASK_HEARTBEAT)
    set(srcs "fault_inject.c")
endif()
idf_component_register(SRCS ${srcs}
                       INCLUDE_DIRS "include"
                       PRIV_REQUIRES console_fmt esp_timer)
