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


def reset_and_capture(bench, slot, after_banner_s=0.0, timeout_s=30.0, all_boots=False):
    """Hard-reset the DUT and return every console line since the reset.

    The bench's reset call takes ~10 s and delivers boot output in one batch
    (testing/test-plan.yaml, dut-console-after-reset), so lines are read from
    the recorded buffer, never from a monitor opened afterwards. Returns the
    first boot's lines once `after_banner_s` of host time has passed after the
    first banner/Init line. With `all_boots`, every line since the reset is
    returned uncut, for tests that must see a second boot.
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
            return lines if all_boots else first_boot(lines)
        time.sleep(0.5)
    lines = fetch(bench, slot, t0)
    return lines if all_boots else first_boot(lines)


def capture_for(bench, slot, seconds, chunk_s=60.0):
    """Read the console for `seconds` of host time without resetting.

    The bench keeps only the last 1000 lines (testing/test-plan.yaml,
    bench-serial-monitor), about 5 minutes of this firmware's output, so a long
    window is read in chunks and joined on the host timestamps.
    """
    t0 = time.time()
    end = t0 + seconds
    out, since = [], t0
    while True:
        time.sleep(max(0.0, min(chunk_s, end - time.time())))
        for ln in fetch(bench, slot, since):
            if ln.ts > since and ln.ts <= end:
                out.append(ln)
        if out:
            since = out[-1].ts
        if time.time() >= end:
            return out


def close_console(bench, slot, seconds):
    """Leave the DUT console unread for `seconds` of host time, then reopen it with DTR/RTS low.

    The bench has no such endpoint: its proxy reads every console permanently
    (testing/test-plan.yaml, bench-serial-port-control). Returns the host times
    of close and reopen once it does.
    """
    import pytest
    pytest.skip("not done: needs bench-serial-port-control — the bench reads every console permanently")
