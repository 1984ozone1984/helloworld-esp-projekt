"""FSD §6 Heartbeat — target tier (testing/test-plan.yaml)."""
import pytest

from console import HEARTBEAT, matches

def _beats(lines):
    return [(ln, int(m.group(1)), int(m.group(2)), int(m.group(3))) for ln, m in matches(lines, HEARTBEAT)]


def test_tc_hb_01_period(steady):
    """TC-HB-01 · FR-HB-01: consecutive heartbeats 950–1050 ms apart (log timestamps), none missing."""
    b = _beats(steady)
    assert len(b) >= 55, f"only {len(b)} heartbeats in 60 s"
    gaps = [(y[1] - x[1], x[2], y[2]) for x, y in zip(b, b[1:])]
    assert all(n2 == n1 + 1 for _, n1, n2 in gaps), "missing heartbeat line"
    bad = [g for g, _, _ in gaps if not 950 <= g <= 1050]
    assert not bad, f"intervals out of band: {bad[:5]}"


def test_tc_hb_02_counter_from_reset(boot):
    """TC-HB-02 · FR-HB-02 (b): after a reset n runs 1..10 with no gaps."""
    n = [x[2] for x in _beats(boot)][:10]
    if len(n) < 10 and n == list(range(1, len(n) + 1)):
        pytest.skip(f"not done: needs bench-single-reset — one boot yields only {len(n)} heartbeats")
    assert n == list(range(1, 11)), n


def test_tc_hb_03_uptime(steady):
    """TC-HB-03 · FR-HB-03: uptime_ms grows 950–1050 between consecutive heartbeats."""
    u = [x[3] for x in _beats(steady)]
    d = [b - a for a, b in zip(u, u[1:])]
    assert d and all(950 <= x <= 1050 for x in d), d[:10]


def test_tc_hb_04_host_rate(steady):
    """TC-HB-04 · NFR-HB-04: 59–61 heartbeats received in 60 s of host time, no bursts."""
    ts = [x[0].ts for x in _beats(steady)]
    assert ts
    window = [t for t in ts if t < ts[0] + 60.0]
    assert 59 <= len(window) <= 61, f"{len(window)} heartbeats in 60 s"
    bursts = [i for i in range(len(ts) - 2) if ts[i + 2] - ts[i] < 0.1]
    assert not bursts, f"{len(bursts)} bursts of >2 lines within 100 ms"
