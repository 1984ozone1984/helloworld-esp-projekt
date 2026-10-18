# helloworld-esp — User Manual

How to install and run helloworld-esp. Every step-by-step operating procedure
lives in this manual and nowhere else. The FSD says what the firmware does;
this manual says how to make it do it.

**Status: development builds only; no release yet.** CI builds the firmware and
it runs on the testbench, but `v0.1.0` is not tagged. Chapters 2–5 are filled in
when the first release ships.

## Contents

1. What you need
2. Installation and first run
3. Configuration
4. Watching the device
5. Troubleshooting
6. Recovery

## 1. What you need

- A Seeed Studio **XIAO ESP32S3 Sense** (8 MB flash). The firmware blinks the
  orange user LED (GPIO21). Leave the microSD slot empty, because GPIO21 is also
  its chip select.
- A USB-C data cable (not charge-only).
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
