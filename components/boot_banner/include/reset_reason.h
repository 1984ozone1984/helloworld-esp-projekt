// Reset-reason names (FSD Appendix A.2). Pure: no ESP-IDF includes.
#pragma once

// Name of an esp_reset_reason_t value; "UNKNOWN" for any value outside A.2.
const char *reset_reason_name(int reason);
