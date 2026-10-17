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

Two fault-injection variants exist, `fault-heartbeat` and `fault-blink`. Each
is selected by its own `sdkconfig.<variant>.defaults`
(`CONFIG_HELLO_FAULT_STALL_TASK_HEARTBEAT=y` or `..._BLINK=y`) through
`SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.<variant>.defaults"`, and
builds into its own build directory. Release images never use them (FSD
FR-BUILD-01). CI builds a variant only from a manual `workflow_dispatch`. A tag
always builds production, and every build greps the `.bin` for
`fault: stalling` in both directions.

## Managed components

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

## CI

| Workflow | Trigger | Does |
|---|---|---|
| `.github/workflows/ci.yml` (host tests) | push to `main`, PR | `cmake -S tests/host -B build-host && ctest --test-dir build-host` |
| `.github/workflows/build.yml` | push to `main`, `v*.*.*` tag, manual | Builds in `espressif/idf:v6.0.2` and uploads `out/` (bin, elf, generated sdkconfig, cold-flash set from `flash_args`). On a tag: `verify` runs the journey (`pytest tests/bench -m journey`) on the self-hosted runner, then `release` publishes |

The `verify` job reads the repository variables `TESTBENCH_URL` and `DUT_SLOT`.
The journey needs no person, so a tag can be verified unattended.

## Devcontainer and runner

`.devcontainer/` builds on `espressif/idf:v6.0.2` and adds pytest, the
`TestbenchDriver` (harness repo pinned by `HARNESS_REF`) and the GitHub Actions
runner. The runner is installed but stays idle until the owner runs
`.devcontainer/runner/register.sh`. After that it registers per-repo,
ephemeral, with labels `self-hosted,testbench`, in a restart loop. It needs
`GH_RUNNER_PAT`, a fine-grained token for this repository with Administration
read/write, passed in from the owner's host environment.
