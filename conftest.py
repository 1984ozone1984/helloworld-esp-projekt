"""Command-line options shared by the target and bench tiers.

pytest reads options only from the root conftest; fixtures live beside the tests.
"""
import os


def pytest_addoption(parser):
    parser.addoption("--coldflash-dir", default=os.environ.get("COLDFLASH_DIR"),
                     help="CI artefact coldflash/ directory (flash_args + images)")
    parser.addoption("--expect-version", default=os.environ.get("EXPECT_VERSION"),
                     help="version the banner must report; default: from the artefact directory name")
