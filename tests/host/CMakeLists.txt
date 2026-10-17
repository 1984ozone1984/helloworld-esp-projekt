# Host tier: pure cores compiled with the host compiler, no ESP-IDF.
cmake_minimum_required(VERSION 3.22)
project(helloworld_host_tests C)
enable_testing()

add_executable(test_tier_runs test_tier_runs.c)
add_test(NAME tier_runs COMMAND test_tier_runs)
