# helloworld-esp — Architecture bindings

How the source mirrors the layering in FSD §2.4. These rules are HOW: none of
them is observable from outside the running device.

## Layers to modules

| Layer | FSD component | Module (ESP-IDF component) | Pure core (host tier) |
|---|---|---|---|
| L2 | Boot banner (§5) | `components/boot_banner` | `reset_reason_name()` |
| L2 | Heartbeat (§6) | `components/heartbeat` | `heartbeat_counter_next()` |
| L2 | Blinker (§7) | `components/blinker` | `blink_toggle()` |
| L1 | Console line format (§8) | `components/console_fmt` | `fmt_banner()`, `fmt_heartbeat()`, `fmt_led()`, `fmt_fault()` |
| L1 | LED driver (§9) | `components/led` | `led_level()` — on → 0, off → 1 (active-low) |
| test | Fault injection (§11) | `components/fault_inject` | — |
| root | Composition | `main/` (`app_main`) | — |

`main/` is the composition root: it initialises the LED driver, emits the
banner, subscribes and starts the two tasks, and wires the fault-injection hook
when it is configured. No other module knows about the composition.

## Rules

- **One component per FSD chapter.** An interface is never folded into the
  feature that uses it.
- **Downward dependencies only.** L2 components may depend on L1 and L0; L1 on
  L0 only. `console_fmt` and `led` never include an L2 header.
- **Pure cores have no ESP-IDF includes.** They take plain C values and return
  plain C values or write into a caller-provided buffer, so `tests/host/` can
  compile them with the host compiler alone.
- **Fault injection is a separate component**, compiled in only when
  `CONFIG_HELLO_FAULT_STALL_TASK` is not `none`. Production modules contain no
  `#ifdef` for it; the hook is registered from `main/`.
- **No PSRAM.** `CONFIG_SPIRAM` stays disabled. The firmware does not need it,
  and a PSRAM mode that does not match the XIAO ESP32S3's octal PSRAM fails at
  boot.

## Test layout

```text
tests/host/      pure cores, plain CMake + compiler, no ESP-IDF
tests/target/    pytest against the DUT console via the testbench (P-SERIAL)
tests/bench/     operator and RF-scan checks via the testbench
```
