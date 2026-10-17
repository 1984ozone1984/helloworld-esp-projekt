// Console line format (FSD §8, Appendix A.1). Pure: no ESP-IDF includes.
// Each fmt_* writes the message body after the ESP-IDF "<L> (<ms>) <tag>: "
// prefix and returns its length, or -1 if `buf` is too small.
#pragma once
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define CONSOLE_TAG_HELLO "hello"
#define CONSOLE_TAG_LED   "led"
#define CONSOLE_TAG_FAULT "fault"

int fmt_banner(char *buf, size_t len, const char *version, const char *reset_reason);
int fmt_heartbeat(char *buf, size_t len, uint32_t n, uint32_t uptime_ms);
int fmt_led(char *buf, size_t len, bool on);
int fmt_fault(char *buf, size_t len, const char *task);
