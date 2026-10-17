"""JRN-01 — the standard run, one test per step, in order (testing/test-plan.yaml).

A workflow test: the order is part of the claim. A step whose predecessor did
not pass is skipped as "not done: precondition", never reported as failed.
Recovery after partial execution: re-run the whole journey from JRN-01.1.
"""
import pytest

from tests.conftest import flash_images
from tests.target.console import BANNER, HEARTBEAT, LED, PANIC_REASONS, PANIC_REPORT, matches, reset_and_capture

pytestmark = pytest.mark.journey

_state = {"passed": set(), "lines": None}


def _needs(step):
    if step not in _state["passed"]:
        pytest.skip(f"not done: precondition — {step} did not pass")


def _done(step):
    _state["passed"].add(step)


def test_jrn_01_1_flash(bench, slot, coldflash):
    """Flash the image: /api/flash ok for every image in flash_args."""
    res = bench.flash(slot, flash_images(coldflash), chip="esp32s3")
    assert res.get("ok"), f"flash failed: {res.get('output', '')[-500:]}"
    _done("JRN-01.1")


def test_jrn_01_2_banner(bench, slot, expected_version):
    """Banner after reset: version is the image's, reset reason is non-panic."""
    _needs("JRN-01.1")
    lines = reset_and_capture(bench, slot, after_banner_s=3.5)
    _state["lines"] = lines
    assert not [ln for ln in lines if PANIC_REPORT.search(ln.text)], "panic report after reset"
    banners = matches(lines, BANNER)
    assert len(banners) == 1, f"expected one banner, got {len(banners)}"
    _, m = banners[0]
    assert int(m.group(1)) <= 3000, f"banner at {m.group(1)} ms after reset"
    assert m.group(2) == expected_version
    assert m.group(3) not in PANIC_REASONS, f"reset_reason={m.group(3)}"
    _done("JRN-01.2")


def test_jrn_01_3_heartbeat(bench, slot):
    """Heartbeat n=1,2,3 within 3.5 s of the banner, 950–1050 ms apart."""
    _needs("JRN-01.2")
    lines = _state["lines"]
    (_, b), = matches(lines, BANNER)
    beats = [m for _, m in matches(lines, HEARTBEAT)][:3]
    assert [int(m.group(2)) for m in beats] == [1, 2, 3]
    t = [int(m.group(1)) for m in beats]
    assert t[2] - int(b.group(1)) <= 3500
    assert all(950 <= d <= 1050 for d in (t[1] - t[0], t[2] - t[1])), t
    _done("JRN-01.3")


def test_jrn_01_4_led(bench, slot):
    """LED lines on/off/on/off within 2.5 s of the banner, 450–550 ms apart."""
    _needs("JRN-01.3")
    lines = _state["lines"]
    (_, b), = matches(lines, BANNER)
    leds = [m for _, m in matches(lines, LED)][:4]
    states = [m.group(2) for m in leds]
    assert len(states) == 4 and all(a != c for a, c in zip(states, states[1:])), states
    t = [int(m.group(1)) for m in leds]
    assert t[3] - int(b.group(1)) <= 2500
    assert all(450 <= c - a <= 550 for a, c in zip(t, t[1:])), t
    _done("JRN-01.4")
