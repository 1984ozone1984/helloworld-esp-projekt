"""FSD §11 NFR-WDT-04, NFR-WDT-05 — RUNNING with and without a host reading, no reset."""
import pytest

from tests.target.console import BANNER, HEARTBEAT, PANIC_REPORT, capture_for, close_console, matches


@pytest.mark.slow
def test_tc_wdt_04_soak_10_min(bench, slot, boot):
    """TC-WDT-04 · NFR-WDT-04: 600 s with no banner, no panic, heartbeat n strictly +1."""
    lines = capture_for(bench, slot, 600.0)
    assert not matches(lines, BANNER), "the device rebooted during the soak"
    assert not [ln.text for ln in lines if PANIC_REPORT.search(ln.text)], "panic report"
    n = [int(m.group(2)) for _, m in matches(lines, HEARTBEAT)]
    assert 598 <= len(n) <= 602, f"{len(n)} heartbeats in 600 s"
    gaps = [(a, b) for a, b in zip(n, n[1:]) if b != a + 1]
    assert not gaps, f"heartbeat counter broke: {gaps[:5]}"


@pytest.mark.slow
def test_tc_wdt_05_console_unread_60_s(bench, slot, boot):
    """TC-WDT-05 · NFR-WDT-05: 60 s with nobody reading the console; n keeps pace with host time, no banner."""
    before = matches(capture_for(bench, slot, 5.0), HEARTBEAT)
    assert before, "no heartbeat before closing the console"
    ln_n, m_n = before[-1]
    n0 = int(m_n.group(2))
    if n0 < 10:
        pytest.skip(f"not done: precondition N >= 10, N = {n0}")
    close_console(bench, slot, 60.0)
    after = capture_for(bench, slot, 5.0)
    beats = matches(after, HEARTBEAT)
    assert beats, "no heartbeat after reopening (the reopen may have halted the chip: test void)"
    ln_m, m_m = beats[0]
    banners = [m.group(3) for ln, m in matches(after, BANNER) if ln.ts <= ln_m.ts]
    assert not banners, f"the device reset while unobserved: reset_reason={banners}"
    gained, elapsed = int(m_m.group(2)) - n0, ln_m.ts - ln_n.ts
    assert abs(gained - elapsed) <= 2, f"n gained {gained} in {elapsed:.1f} s host time: counts lost"
