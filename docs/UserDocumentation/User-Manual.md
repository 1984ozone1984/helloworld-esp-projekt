# helloworld-esp — User Manual

How to install and run helloworld-esp. Every step-by-step operating procedure
lives in this manual and nowhere else. The FSD says what the firmware does;
this manual says how to make it do it.

**Status: nothing is deployable yet.** The FSD is baselined and no firmware has
been built. Chapters 2–5 are filled in as the build phases deliver.

## Contents

1. What you need
2. Installation and first run
3. Configuration
4. Watching the device
5. Troubleshooting
6. Recovery

## 1. What you need

- An ESP32-S3-DevKitC-1 board, module **N8R8** (8 MB flash), revision v1.0
  (RGB LED on GPIO48).
- A USB cable to the board's port labelled **USB**, not the one labelled **UART**.
- Either a testbench slot, or a Linux/macOS/Windows PC with Docker to run the
  `espressif/idf:v6.0.2` build container.
- No accounts, credentials, or network access are needed to run the device.

## 2. Installation and first run

Not yet available — delivered with build Phase 1.

## 3. Configuration

There is nothing to configure at runtime. All settings are fixed at build time
(FSD §12).

## 4. Watching the device

Not yet available — delivered with build Phase 1. When you open the console
yourself, open it with DTR and RTS low. Otherwise the chip stops and looks hung.

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Console opens but shows nothing, and the LED stops changing | The terminal asserted DTR/RTS on open, so the chip is in download mode or held in reset | Reopen with DTR and RTS low; press **RST** once |

## 6. Recovery

Reflash the release image over USB. The firmware stores nothing, so a reflash
fully restores it.

---

**Contract:** [`../Functionality/FSD.md`](../Functionality/FSD.md) · **Build rules:** [`../Method/AI-Workflow.md`](../Method/AI-Workflow.md)
