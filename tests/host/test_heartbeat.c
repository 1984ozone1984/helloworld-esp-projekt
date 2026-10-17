// TC-HB-02-host — FSD FR-HB-02 (a): the counter starts at 1 and steps by 1.
#include "check.h"
#include "heartbeat_core.h"

int main(void)
{
    heartbeat_counter_t c;
    heartbeat_counter_init(&c);
    CHECK(heartbeat_counter_next(&c) == 1);
    CHECK(heartbeat_counter_next(&c) == 2);
    CHECK(heartbeat_counter_next(&c) == 3);
    heartbeat_counter_init(&c);   // a reset starts again at 1
    CHECK(heartbeat_counter_next(&c) == 1);
    return CHECK_DONE();
}
