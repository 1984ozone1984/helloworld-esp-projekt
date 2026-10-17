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


def fetch(bench, slot, since, lines=2000):
    res = bench.serial_output(slot=slot, lines=lines, since=since)
    return [Line(e["ts"], e["text"]) for e in res.get("lines") or []]


def matches(lines, rx):
    return [(ln, m) for ln in lines if (m := ln.match(rx))]


def reset_and_capture(bench, slot, after_banner_s=0.0, timeout_s=30.0):
    """Hard-reset the DUT and return every console line since the reset.

    The bench's reset call takes ~10 s and delivers boot output in one batch
    (testing/test-plan.yaml, dut-console-after-reset), so lines are read from
    the recorded buffer, never from a monitor opened afterwards. Returns once
    `after_banner_s` of output after the first banner/Init line is available.
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
            return lines
        time.sleep(0.5)
    return fetch(bench, slot, t0)


def capture_for(bench, slot, seconds):
    """Read the console for `seconds` of host time without resetting."""
    t0 = time.time()
    time.sleep(seconds)
    return fetch(bench, slot, t0)
