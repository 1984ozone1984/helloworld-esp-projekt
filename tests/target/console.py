"""Console line grammar (FSD Appendix A) and capture through the testbench.

Pure parsing lives here so every target test reads lines the same way.
"""
import re
import time
from dataclasses import dataclass

# FSD A.1 — the regex applies after stripping the trailing CR/LF.
BANNER = re.compile(r"^I \((\d+)\) hello: Hello world! version=(\S+) chip=esp32s3 reset_reason=([A-Z_]+)$")
HEARTBEAT = re.compile(r"^I \((\d+)\) hello: heartbeat n=([1-9]\d*) uptime_ms=(\d+)$")
LED = re.compile(r"^I \((\d+)\) led: state=(on|off)$")
FAULT = re.compile(r"^W \((\d+)\) fault: stalling (blink|heartbeat) task$")
# Any line from the normative tags, to check that nothing malformed slips through.
NORMATIVE_TAG = re.compile(r"^[EWIDV] \(\d+\) (hello|led|fault): ")
# FSD A.2
RESET_REASONS = {"UNKNOWN", "POWERON", "EXT", "SW", "PANIC", "INT_WDT", "TASK_WDT", "WDT",
                 "DEEPSLEEP", "BROWNOUT", "SDIO", "USB", "JTAG", "EFUSE", "PWR_GLITCH",
                 "CPU_LOCKUP"}
PANIC_REASONS = {"PANIC", "INT_WDT", "TASK_WDT", "WDT", "UNKNOWN"}
PANIC_REPORT = re.compile(r"Guru Meditation|abort\(\) was called|Task watchdog got triggered|Backtrace:")


@dataclass
class Line:
    ts: float      # host receive time (bench clock)
    text: str

    def match(self, rx):
        return rx.match(self.text.rstrip("\r\n"))


def fetch(bench, slot, since, lines=5000):
    res = bench.serial_output(slot=slot, lines=lines, since=since)
    return [Line(e["ts"], e["text"]) for e in res.get("lines") or []]


def matches(lines, rx):
    return [(ln, m) for ln in lines if (m := ln.match(rx))]


DEVICE_TS = re.compile(r"^[EWIDV] \((\d+)\) ")


def first_boot(lines):
    """Lines of the first boot only.

    One bench reset currently produces two chip resets on this native-USB part
    (testing/test-plan.yaml, bench-single-reset), and the second boot's first
    seconds are lost. A new boot shows as a ROM banner or as the device
    timestamp jumping backwards; everything from there on is cut.
    """
    out, last, seen_rom = [], -1, False
    for ln in lines:
        t = ln.text.rstrip("\r\n")
        if t.startswith("ESP-ROM:"):
            if seen_rom:
                break
            seen_rom = True
        m = DEVICE_TS.match(t)
        if m:
            ms = int(m.group(1))
            if ms + 500 < last:
                break
            last = max(last, ms)
        out.append(ln)
    return out


def reset_and_capture(bench, slot, after_banner_s=0.0, timeout_s=30.0):
    """Hard-reset the DUT and return every console line since the reset.

    The bench's reset call takes ~10 s and delivers boot output in one batch
    (testing/test-plan.yaml, dut-console-after-reset), so lines are read from
    the recorded buffer, never from a monitor opened afterwards. Returns the
    first boot's lines once `after_banner_s` of host time has passed after the
    first banner/Init line.
    """
    t0 = time.time()
    bench.serial_reset(slot=slot)
    deadline = t0 + timeout_s
    first = None
    while time.time() < deadline:
        lines = fetch(bench, slot, t0)
        for ln in lines:
            if ln.match(BANNER) or "Init complete" in ln.text:
                first = first or ln
        if first and lines[-1].ts - first.ts >= after_banner_s:
            return first_boot(lines)
        time.sleep(0.5)
    return first_boot(fetch(bench, slot, t0))


def capture_for(bench, slot, seconds):
    """Read the console for `seconds` of host time without resetting."""
    t0 = time.time()
    time.sleep(seconds)
    return fetch(bench, slot, t0)
