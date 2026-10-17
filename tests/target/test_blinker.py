"""FSD §7 Blinker — target tier (testing/test-plan.yaml)."""
import pytest

from tests.target.console import LED, matches

def _leds(lines):
    return [(int(m.group(1)), m.group(2)) for _, m in matches(lines, LED)]


def test_tc_led_01_toggle_period(steady):
    """TC-LED-01 · FR-LED-01: LED lines 450–550 ms apart (log timestamps)."""
    t = [x[0] for x in _leds(steady)]
    assert len(t) >= 110, f"only {len(t)} LED lines in 60 s"
    d = [b - a for a, b in zip(t, t[1:])]
    bad = [x for x in d if not 450 <= x <= 550]
    assert not bad, f"intervals out of band: {bad[:5]}"


def test_tc_led_02_alternates(steady):
    """TC-LED-02 · FR-LED-02 (b): consecutive LED lines alternate on/off."""
    s = [x[1] for x in _leds(steady)]
    assert s
    same = [i for i in range(len(s) - 1) if s[i] == s[i + 1]]
    assert not same, f"{len(same)} repeated states, first at {same[0]}"
