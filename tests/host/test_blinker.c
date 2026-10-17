// TC-LED-02-host — FSD FR-LED-02 (a): toggling from off alternates on/off.
// TC-CON-05-host — FSD CON-05 (a): active-low, on -> 0, off -> 1.
#include "blink_core.h"
#include "check.h"
#include "led_core.h"

int main(void)
{
    bool s = false;
    bool want[] = {true, false, true, false};
    for (int i = 0; i < 4; i++) {
        s = blink_toggle(s);
        CHECK(s == want[i]);
    }
    CHECK(led_level(true) == 0);
    CHECK(led_level(false) == 1);
    return CHECK_DONE();
}
