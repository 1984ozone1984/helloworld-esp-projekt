"""DUT fixtures for the target and bench tiers: the testbench, the DUT slot, the image.

Target and bench tiers need TestbenchDriver on PYTHONPATH (the devcontainer sets it; locally point it
at Embedded-AI-Harness/pytest at the commit pinned in .devcontainer/Dockerfile).
"""
import os
import re
from pathlib import Path

import pytest

PLAN = Path(__file__).resolve().parents[1] / "testing" / "test-plan.yaml"


def _plan_value(key):
    m = re.search(rf"^\s+{key}:\s*\"?([^\"\s#]+)", PLAN.read_text(), re.M)
    return m.group(1) if m else None


@pytest.fixture(scope="session")
def bench():
    url = os.environ.get("TESTBENCH_URL")
    if not url:
        pytest.skip("not done: TESTBENCH_URL unset")
    # Imported here so the artefact tier (CI, no driver) can share this conftest.
    from testbench_driver import TestbenchDriver
    with TestbenchDriver(url) as tb:
        try:
            tb.info()
        except Exception as e:  # unreachable bench = unmet precondition
            pytest.skip(f"not done: testbench unreachable at {url}: {e}")
        yield tb


@pytest.fixture(scope="session")
def slot(bench):
    """The slot holding the DUT, found by MAC; slot labels move when the bench restarts."""
    if os.environ.get("DUT_SLOT"):
        return os.environ["DUT_SLOT"]
    mac = _plan_value("mac")
    present = [s["label"] for s in bench.get_devices() if s.get("present")]
    for label in present:
        if bench.chip_info(label).get("mac", "").lower() == mac:
            return label
    pytest.skip(f"not done: no present slot reports DUT MAC {mac} (present: {present})")


@pytest.fixture(scope="session")
def coldflash(request):
    d = request.config.getoption("--coldflash-dir")
    if not d or not (Path(d) / "flash_args").is_file():
        pytest.skip("not done: no --coldflash-dir with flash_args")
    return Path(d)


@pytest.fixture(scope="session")
def expected_version(request, coldflash):
    v = request.config.getoption("--expect-version")
    if v:
        return v
    m = re.match(r"firmware-(.+)$", coldflash.resolve().parent.name)
    if not m:
        pytest.skip("not done: pass --expect-version (artefact dir is not firmware-<version>)")
    return m.group(1)


def flash_images(coldflash):
    """Offsets come from flash_args, never from memory."""
    images = {}
    for line in (coldflash / "flash_args").read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].startswith("0x"):
            images[parts[0]] = str(coldflash / Path(parts[1]).name)
    return images


@pytest.fixture(scope="session")
def image(bench, slot, coldflash):
    """The artefact under test, flashed once per session."""
    res = bench.flash(slot, flash_images(coldflash), chip="esp32s3")
    if not res.get("ok"):
        pytest.skip(f"not done: precondition — flash failed: {res.get('output', '')[-300:]}")
    return coldflash


@pytest.fixture(scope="session")
def boot(bench, slot, image):
    """Console lines from one hard reset, including 11 s after the banner."""
    from tests.target.console import reset_and_capture
    return reset_and_capture(bench, slot, after_banner_s=11.0)


@pytest.fixture(scope="session")
def steady(bench, slot, boot):
    """60 s of console lines from a device already RUNNING (shared setup, P-SERIAL)."""
    from tests.target.console import capture_for
    return capture_for(bench, slot, 60.0)

