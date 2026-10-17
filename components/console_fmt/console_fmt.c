#include "console_fmt.h"

#include <inttypes.h>
#include <stdio.h>

static int fit(int written, size_t len)
{
    return (written < 0 || (size_t)written >= len) ? -1 : written;
}

int fmt_banner(char *buf, size_t len, const char *version, const char *reset_reason)
{
    return fit(snprintf(buf, len, "Hello world! version=%s chip=esp32s3 reset_reason=%s",
                        version, reset_reason), len);
}

int fmt_heartbeat(char *buf, size_t len, uint32_t n, uint32_t uptime_ms)
{
    return fit(snprintf(buf, len, "heartbeat n=%" PRIu32 " uptime_ms=%" PRIu32, n, uptime_ms), len);
}

int fmt_led(char *buf, size_t len, bool on)
{
    return fit(snprintf(buf, len, "state=%s", on ? "on" : "off"), len);
}

int fmt_fault(char *buf, size_t len, const char *task)
{
    return fit(snprintf(buf, len, "stalling %s task", task), len);
}
