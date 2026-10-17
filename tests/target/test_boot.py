"""FSD §5 Boot banner and §2.2 CON-04 — target tier (testing/test-plan.yaml)."""
import pytest

from console import BANNER, PANIC_REPORT, matches

NON_PANIC = {"POWERON", "EXT", "SW", "USB", "JTAG"}


def _one_banner(boot):
    banners = matches(boot, BANNER)
    assert len(banners) == 1, f"expected one banner for one reset, got {len(banners)}"
    return banners[0]


def test_tc_boot_01_banner_within_3s(boot):
    """TC-BOOT-01 · FR-BOOT-01: one banner, log timestamp ≤ 3000 ms, no panic before it."""
    ln, m = _one_banner(boot)
    before = boot[: boot.index(ln)]
    assert not [x for x in before if PANIC_REPORT.search(x.text)], "panic report before the banner"
    assert int(m.group(1)) <= 3000, f"banner at {m.group(1)} ms"


def test_tc_boot_02_version_is_the_images(boot, expected_version):
    """TC-BOOT-02 · FR-BOOT-02: version equals git describe of the image's source."""
    _, m = _one_banner(boot)
    v = m.group(2)
    assert v != "1", "IDF fallback version"
    assert v == expected_version


def test_tc_boot_03_reset_reason_after_bench_reset(boot):
    """TC-BOOT-03 · FR-BOOT-03 (b): a bench hard reset reports a non-panic reason."""
    _, m = _one_banner(boot)
    assert m.group(3) in NON_PANIC, f"reset_reason={m.group(3)}"


def test_tc_con_04_console_is_usb_serial_jtag(bench, slot, boot):
    """TC-CON-04 · CON-04: the banner arrives on the slot's USB-Serial/JTAG port."""
    s = bench.get_slot(slot)
    products = [u.get("product", "") for u in s.get("usb_devices") or []]
    assert any("USB JTAG/serial" in p for p in products), products
    _one_banner(boot)


def test_tc_con_02_dut_flash_size(bench, slot, image):
    """TC-CON-02 · CON-02 (b): the DUT reports at least 8 MB of flash."""
    info = bench.chip_info(slot)
    size = info.get("flash_size", "")
    assert size.endswith("MB") and int(size[:-2]) >= 8, info
