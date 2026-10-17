"""FSD §14 NFR-SEC-01 (b) — the device advertises no BLE (bench tier)."""
import re
from pathlib import Path

import pytest

PLAN = Path(__file__).resolve().parents[2] / "testing" / "test-plan.yaml"


def _base_mac():
    m = re.search(r'^\s+mac: "([0-9a-f:]{17})"', PLAN.read_text(), re.M)
    return int(m.group(1).replace(":", ""), 16)


def _derived(base):
    # ESP32-S3: STA = base, AP = base+1, BT = base+2, Ethernet = base+3.
    return {":".join(f"{(base + k) >> s & 0xFF:02x}" for s in range(40, -8, -8)) for k in range(4)}


def _norm(addr):
    return (addr or "").lower()


def test_tc_sec_01_ble_silent(bench, image):
    """TC-SEC-01 · NFR-SEC-01 (b): no BLE address within base MAC .. base+3 over 30 s."""
    dut = _derived(_base_mac())
    seen = {_norm(d.get("address")) for d in bench.ble_scan(timeout=30)}
    # A silent result proves nothing unless the instrument saw something else.
    if not seen:
        pytest.skip("not done: no positive control (no BLE devices seen)")
    assert not dut & seen, f"DUT BLE address seen: {dut & seen}"
