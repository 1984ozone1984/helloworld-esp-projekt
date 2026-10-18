# helloworld-esp — Debugging agenda

Project-side parts that have never been observed doing their job on this
testbench. `/commission` burns this list down. Each item matches a capability
in `testing/test-plan.yaml` marked `available: unproven`; proving the item
flips that capability to `yes`. All items are closed. Measurements belong on the capability, not in
the plan's tests. The testbench itself is not on this list.

| # | Part | Unproven because | Proven by | Capability | Closed |
|---|---|---|---|---|---|
| 1 | XIAO ESP32S3 Sense on its bench slot | This unit has never been on this bench | It enumerates as an ESP32-S3 with 8 MB flash, the skeleton is flashed through `/api/flash` from a CI artefact's `flash_args`, and `Init complete` is observed | `dut-on-slot` | 2026-10-17 · yes: SLOT1, ESP32-S3 v0.2, 8 MB, MAC 30:30:f9:34:72:28; CI run 39057559541 flashed at flash_args offsets; `Init complete` observed after 5/5 resets, then ON/OFF |
| 2 | Console output after reset | The native USB port re-enumerates on reset, so boot output can be lost before the bench reattaches (FSD §4 risk) | `Init complete`, the first line after a bench reset, is captured on 5 of 5 resets | `dut-console-after-reset` | 2026-10-17 · yes: 5/5 resets captured `Init complete` |
| 3 | User LED on GPIO21 | The active-low polarity comes from Seeed's documentation, not from this board | With GPIO21 driven low the operator sees the orange LED lit; driven high, dark | `dut-user-led` | 2026-10-17 · no, by decision: no instrument can see GPIO21; FSD 0.1.3 made FR-LED-03 a human acceptance |
| 4 | Operator at the bench | Nobody has answered a bench prompt for this project | A test prompt is answered yes and no from the portal UI, and both answers reach the caller | `operator` | 2026-10-17 · yes: Done → confirmed true, Cancel → confirmed false |
| 5 | Console output after a firmware-initiated reset | Only bench-issued resets were observed (item 2); a panic reset re-enumerates the native USB without the bench knowing, and FR-WDT-01's "panic report → banner ≤ 3 s (host clock)" rests on catching it (FSD 0.1.7 §3.2) | With an image that resets itself after a known delay, the panic report and the next banner are both captured, with host timestamps, on 5 of 5 resets | `dut-console-after-panic-reset` | 2026-10-18 · yes: 9/9 abort cycles captured from the panic report through the next banner (reset_reason=PANIC), 0.13–0.14 s apart; rst:0xc is a CPU reset, the USB link stays up |
