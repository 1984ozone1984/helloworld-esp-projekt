# helloworld-esp — Build bindings

## Toolchain

- ESP-IDF **v6.0.2**, always built inside `espressif/idf:v6.0.2` so local, CI
  and release builds use the same toolchain (FSD CON-01).
- `cmake_minimum_required(VERSION 3.22)` — 3.16 from a 5.x template fails to
  configure on v6.
- Target set once: `idf.py set-target esp32s3`.

## Configuration

`sdkconfig` is generated and not committed. `sdkconfig.defaults` is committed and
carries every value the FSD states, so nothing is left to a toolchain default:

```text
CONFIG_IDF_TARGET="esp32s3"
CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y
CONFIG_PARTITION_TABLE_SINGLE_APP=y
CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y
CONFIG_LOG_COLORS=n
CONFIG_ESP_TASK_WDT_EN=y
CONFIG_ESP_TASK_WDT_INIT=y
CONFIG_ESP_TASK_WDT_TIMEOUT_S=5
CONFIG_ESP_TASK_WDT_PANIC=y
CONFIG_SPIRAM=n
```

The fault-injection variant adds `sdkconfig.fault.defaults`
(`CONFIG_HELLO_FAULT_STALL_TASK_HEARTBEAT=y` or `..._BLINK=y`) through
`SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.fault.defaults"` and builds
into its own build directory. Release images never use it (FSD FR-BUILD-01).

## Managed components

- `espressif/led_strip` is declared in `main/idf_component.yml` (or the `led`
  component's manifest).
- `dependencies.lock` is committed; `managed_components/` is not.
- Declare `REQUIRES`/`PRIV_REQUIRES` only for what the code includes today. A
  speculative requirement fails at configure time and names the component, not
  the speculation.
- After adding a manifest to an already-configured tree, run
  `idf.py reconfigure` or delete `build/`, because the cached configure skips
  the component solver.

## Versioning

- The image version is ESP-IDF's `PROJECT_VER`, taken from
  `git describe --always --tags --dirty` (FSD FR-BOOT-02). Do not set
  `PROJECT_VER` by hand.
- Releases are annotated tags `vMAJOR.MINOR.PATCH`, built from a clean checkout.
