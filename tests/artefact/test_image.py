"""FSD §2.2 CON-01, CON-02 (a), CON-03, CON-06 and §13 FR-BUILD-01 — read from the image bytes and its sdkconfig.

Formats: ESP-IDF app image header, esp_app_desc_t, and the partition table
(docs.espressif.com, "App Image Format" and "Partition Tables").
"""
import struct

ESP32S3_CHIP_ID = 9
FLASH_SIZE_CODE = {0: "1MB", 1: "2MB", 2: "4MB", 3: "8MB", 4: "16MB"}
APP_DESC_MAGIC = 0xABCD5432


def _app_desc(app_bin):
    # 24-byte image header + 8-byte first-segment header, then esp_app_desc_t.
    magic, = struct.unpack_from("<I", app_bin, 32)
    assert magic == APP_DESC_MAGIC, "no esp_app_desc_t at the start of the first segment"
    field = lambda off, n: app_bin[32 + off:32 + off + n].split(b"\0")[0].decode()
    return {"version": field(16, 32), "project": field(48, 32), "idf_ver": field(112, 32)}


def _partitions(table):
    out = []
    for i in range(0, len(table), 32):
        e = table[i:i + 32]
        if e[:2] != b"\xaa\x50":
            break
        _, ptype, sub, off, size = struct.unpack_from("<HBBII", e)
        out.append((e[12:28].split(b"\0")[0].decode(), ptype, sub, off, size))
    return out


def test_tc_con_01_chip_and_idf(app_bin):
    """TC-CON-01 · CON-01: built for esp32s3 with ESP-IDF v6.0.2."""
    assert app_bin[0] == 0xE9, "not an ESP image"
    chip_id, = struct.unpack_from("<H", app_bin, 12)
    assert chip_id == ESP32S3_CHIP_ID, f"chip id {chip_id}"
    assert _app_desc(app_bin)["idf_ver"].startswith("v6.0.2")


def test_tc_con_02_header_flash_size(app_bin):
    """TC-CON-02-host · CON-02 (a): the image header says 8 MB flash."""
    assert FLASH_SIZE_CODE.get(app_bin[3] >> 4) == "8MB", hex(app_bin[3])


def test_tc_con_03_partitions_and_size(app_bin, partition_bin):
    """TC-CON-03 · CON-03: single-factory layout at the stated offsets; app <= 1 MB."""
    parts = [(n, off, size) for n, _, _, off, size in _partitions(partition_bin)]
    assert parts == [("nvs", 0x9000, 0x6000), ("phy_init", 0xF000, 0x1000),
                     ("factory", 0x10000, 0x100000)], parts
    assert len(app_bin) <= 1_048_576, f"app is {len(app_bin)} bytes"


def test_tc_build_01_no_fault_path(app_bin):
    """TC-BUILD-01 · FR-BUILD-01: the release image contains no fault-injection path."""
    assert b"fault: stalling" not in app_bin
    assert b"stalling %s task" not in app_bin


RADIO_SYMBOLS = (b"esp_wifi_init", b"esp_phy_enable", b"esp_bt_controller_init", b"nimble_port_init")
LINKED_SYMBOLS = (b"app_main", b"esp_reset_reason")


def test_tc_sec_01_no_radio_stack(app_elf):
    """TC-SEC-01-host · NFR-SEC-01 (a): no WiFi, PHY or Bluetooth stack is linked."""
    missing = [s for s in LINKED_SYMBOLS if b"\0" + s + b"\0" not in app_elf]
    assert not missing, f"positive control failed, symbol table unreadable: {missing}"
    linked = [s.decode() for s in RADIO_SYMBOLS if b"\0" + s + b"\0" in app_elf]
    assert not linked, f"radio stack linked: {linked}"


def test_tc_con_06_no_psram(sdkconfig):
    """TC-CON-06 · CON-06: the generated sdkconfig leaves CONFIG_SPIRAM unset."""
    assert "CONFIG_IDF_TARGET=\"esp32s3\"" in sdkconfig, "not this project's sdkconfig"
    assert "CONFIG_SPIRAM=y" not in sdkconfig.splitlines(), "PSRAM enabled"
