"""FSD §11 NFR-WDT-04 — 10 minutes RUNNING with a host reading, no reset."""
import pytest

from console import BANNER, HEARTBEAT, PANIC_REPORT, capture_for, matches


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
