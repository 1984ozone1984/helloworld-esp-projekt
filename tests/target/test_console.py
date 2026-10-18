"""FSD §8 Console line format — target tier (testing/test-plan.yaml)."""
import pytest

from tests.target.console import BANNER, FAULT, HEARTBEAT, LED, NORMATIVE_TAG, matches

GRAMMAR = (BANNER, HEARTBEAT, LED, FAULT)


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


def test_tc_log_03_fault_line_on_usb(request, bench, slot, image):
    """TC-LOG-03 · FR-LOG-01/02 (c): a fault image's fault line arrives on USB and matches A.1."""
    from pathlib import Path
    from tests.conftest import flash_images
    from tests.target.console import capture_for
    d = request.config.getoption("--fault-coldflash-dir")
    if not d or not (Path(d) / "flash_args").is_file():
        pytest.skip("not done: no --fault-coldflash-dir with flash_args")
    try:
        assert bench.flash(slot, flash_images(Path(d)), chip="esp32s3").get("ok"), "fault image flash failed"
        lines = capture_for(bench, slot, 15.0)
    finally:
        assert bench.flash(slot, flash_images(image), chip="esp32s3").get("ok"), "release image not restored"
    tagged = [ln.text.rstrip("\r\n") for ln in lines if " fault: " in ln.text]
    assert tagged, "no fault-tagged line on the USB console"
    assert all(FAULT.match(t) for t in tagged), f"fault line not matching A.1: {tagged}"
