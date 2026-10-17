"""FSD §8 Console line format — target tier (testing/test-plan.yaml)."""
import pytest

from console import BANNER, FAULT, HEARTBEAT, LED, NORMATIVE_TAG, matches

GRAMMAR = (BANNER, HEARTBEAT, LED, FAULT)


@pytest.mark.xfail(reason="heartbeat and blinker not implemented (FSD §6, §7)", strict=False)
def test_tc_log_01_lines_on_usb_console(boot):
    """TC-LOG-01 · FR-LOG-01: banner, heartbeat and LED lines all arrive on the USB console."""
    assert matches(boot, BANNER), "no banner"
    assert matches(boot, HEARTBEAT), "no heartbeat"
    assert matches(boot, LED), "no LED line"


def test_tc_log_02_every_normative_line_matches(boot, steady):
    """TC-LOG-02 · FR-LOG-02 (b): every hello/led/fault line matches A.1, no escapes."""
    lines = boot + steady
    normative = [ln for ln in lines if NORMATIVE_TAG.match(ln.text.rstrip("\r\n"))]
    assert normative, "no normative lines captured"
    bad = [ln.text for ln in normative if not any(ln.match(rx) for rx in GRAMMAR)]
    assert not bad, bad[:5]
    assert not [ln.text for ln in lines if "\x1b" in ln.text], "ANSI escape in console output"
