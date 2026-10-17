"""Host-tier checks on the built artefact: the coldflash/ set from CI."""
import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def coldflash(request):
    d = request.config.getoption("--coldflash-dir") or os.environ.get("COLDFLASH_DIR")
    if not d or not (Path(d) / "flash_args").is_file():
        pytest.skip("not done: no COLDFLASH_DIR with flash_args")
    return Path(d)


@pytest.fixture(scope="session")
def app_bin(coldflash):
    return (coldflash / "helloworld-esp.bin").read_bytes()


@pytest.fixture(scope="session")
def partition_bin(coldflash):
    return (coldflash / "partition-table.bin").read_bytes()


@pytest.fixture(scope="session")
def app_elf(coldflash):
    elfs = sorted(coldflash.parent.glob("firmware_*.elf"))
    if not elfs:
        pytest.skip("not done: no firmware_*.elf beside coldflash/")
    return elfs[0].read_bytes()
