# Host tier: pure cores compiled with the host compiler, no ESP-IDF.
cmake_minimum_required(VERSION 3.22)
project(helloworld_host_tests C)
enable_testing()

set(COMPONENTS ${CMAKE_CURRENT_SOURCE_DIR}/../../components)

add_executable(test_tier_runs test_tier_runs.c)
add_test(NAME tier_runs COMMAND test_tier_runs)

add_executable(test_console_fmt test_console_fmt.c ${COMPONENTS}/console_fmt/console_fmt.c)
target_include_directories(test_console_fmt PRIVATE ${COMPONENTS}/console_fmt/include)
add_test(NAME console_fmt COMMAND test_console_fmt)

add_executable(test_reset_reason test_reset_reason.c ${COMPONENTS}/boot_banner/reset_reason.c)
target_include_directories(test_reset_reason PRIVATE ${COMPONENTS}/boot_banner/include)
add_test(NAME reset_reason COMMAND test_reset_reason)

add_executable(test_heartbeat test_heartbeat.c ${COMPONENTS}/heartbeat/heartbeat_core.c)
target_include_directories(test_heartbeat PRIVATE ${COMPONENTS}/heartbeat/include)
add_test(NAME heartbeat COMMAND test_heartbeat)

add_executable(test_blinker test_blinker.c ${COMPONENTS}/blinker/blink_core.c ${COMPONENTS}/led/led_core.c)
target_include_directories(test_blinker PRIVATE ${COMPONENTS}/blinker/include ${COMPONENTS}/led/include)
add_test(NAME blinker COMMAND test_blinker)
