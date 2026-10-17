#!/usr/bin/env python3
"""Write test results into testing/test-plan.yaml from JUnit XML.

Usage: record_results.py --commit <sha> <junit.xml> [<junit.xml> ...]

Matches each plan entry by its `impl:` — pytest `path::func`, or a host test
`tests/host/test_<name>.c` against the CTest test `<name>`. Writes `status`
(successful | failed | not done), `reason` and `commit`. Entries with no result
in the given files are left untouched; deprecated entries are never touched.
"""
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PLAN = Path(__file__).resolve().parents[1] / "testing" / "test-plan.yaml"


def junit_results(paths):
    out = {}
    for p in paths:
        for tc in ET.parse(p).getroot().iter("testcase"):
            cls, name = tc.get("classname", ""), tc.get("name", "")
            key = f"{cls.replace('.', '/')}.py::{name}" if cls.startswith("tests.") else name
            failure = tc.find("failure")
            if failure is None:
                failure = tc.find("error")
            skipped = tc.find("skipped")
            if failure is not None:
                out[key] = ("failed", (failure.get("message") or "failed").splitlines()[0][:160])
            elif skipped is not None:
                msg = (skipped.get("message") or "").splitlines()[0] if skipped.get("message") else ""
                if skipped.get("type") == "pytest.xfail":
                    msg = "feature not implemented (xfail): " + msg
                out[key] = ("not done", msg[:160] or "skipped")
            else:
                out[key] = ("successful", None)
    return out


def impl_key(impl):
    m = re.match(r"tests/host/test_(\w+)\.c$", impl)
    return m.group(1) if m else impl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", required=True)
    ap.add_argument("junit", nargs="+")
    a = ap.parse_args()
    results = junit_results(a.junit)
    text = PLAN.read_text()
    blocks = re.split(r"(?m)^(?=  - id: )", text)
    changed = 0
    for i, b in enumerate(blocks):
        im = re.search(r"(?m)^    impl: (\S+)$", b)
        if not im or re.search(r"(?m)^    status: deprecated$", b):
            continue
        res = results.get(impl_key(im.group(1)))
        if not res:
            continue
        status, reason = res
        b = re.sub(r"(?m)^    status: .*$", f"    status: {status}", b)
        b = re.sub(r"(?m)^    reason: .*\n", "", b)
        b = re.sub(r"(?m)^    commit: .*\n", "", b)
        tail = f"    commit: {a.commit}\n" + (f"    reason: {reason!r}\n" if reason else "")
        b = re.sub(r"(?m)^(    status: .*\n)", lambda m: m.group(1) + tail, b, count=1)
        blocks[i] = b
        changed += 1
    PLAN.write_text("".join(blocks))
    print(f"recorded {changed} results at {a.commit}")


if __name__ == "__main__":
    main()
