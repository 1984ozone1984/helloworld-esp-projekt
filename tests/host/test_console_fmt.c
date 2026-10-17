// TC-LOG-02-host — FSD FR-LOG-02 (a): each line body matches FSD Appendix A.1.
// The "<L> (<ms>) <tag>: " prefix is ESP-IDF's; the bodies are ours.
#include "check.h"
#include "console_fmt.h"

int main(void)
{
    char buf[160];

    CHECK(fmt_banner(buf, sizeof buf, "v0.1.0", "POWERON") > 0);
    CHECK_STR(buf, "Hello world! version=v0.1.0 chip=esp32s3 reset_reason=POWERON");

    CHECK(fmt_heartbeat(buf, sizeof buf, 1, 1137) > 0);
    CHECK_STR(buf, "heartbeat n=1 uptime_ms=1137");
    CHECK(fmt_heartbeat(buf, sizeof buf, 4294967295u, 4294967295u) > 0);
    CHECK_STR(buf, "heartbeat n=4294967295 uptime_ms=4294967295");

    CHECK(fmt_led(buf, sizeof buf, true) > 0);
    CHECK_STR(buf, "state=on");
    CHECK(fmt_led(buf, sizeof buf, false) > 0);
    CHECK_STR(buf, "state=off");

    CHECK(fmt_fault(buf, sizeof buf, "heartbeat") > 0);
    CHECK_STR(buf, "stalling heartbeat task");

    // No escape bytes, no trailing space, in any body.
    const char *bodies[] = {"banner", "heartbeat", "led", "fault"};
    for (unsigned i = 0; i < 4; i++) {
        switch (i) {
        case 0: fmt_banner(buf, sizeof buf, "c2761e2", "USB"); break;
        case 1: fmt_heartbeat(buf, sizeof buf, 7, 7000); break;
        case 2: fmt_led(buf, sizeof buf, true); break;
        default: fmt_fault(buf, sizeof buf, "blink"); break;
        }
        CHECK(strchr(buf, 0x1b) == NULL);
        size_t n = strlen(buf);
        if (n == 0 || buf[n - 1] == ' ') {
            printf("FAIL: %s body empty or ends in a space\n", bodies[i]);
            check_failures++;
        }
    }

    // Truncation is reported, never a silently cut line.
    char tiny[8];
    CHECK(fmt_banner(tiny, sizeof tiny, "v0.1.0", "POWERON") < 0);

    CHECK_STR(CONSOLE_TAG_HELLO, "hello");
    CHECK_STR(CONSOLE_TAG_LED, "led");
    CHECK_STR(CONSOLE_TAG_FAULT, "fault");
    return CHECK_DONE();
}
