"""Arbitrage detection tests."""

import pytest

from arbfinder.detect import find_arbitrage


def test_detects_two_way_arb():
    # 2.10 and 2.10 -> implied 0.952 -> ~5% arb
    opp = find_arbitrage([2.10, 2.10])
    assert opp.is_arb
    assert opp.arb_percent == pytest.approx(0.05, abs=0.005)


def test_no_arb_on_vigged_market():
    opp = find_arbitrage([1.91, 1.91])  # standard -110/-110, ~4.5% hold
    assert not opp.is_arb
    assert opp.arb_percent < 0


def test_three_way_arb():
    opp = find_arbitrage([3.5, 3.6, 3.7])
    assert opp.implied == pytest.approx(1/3.5 + 1/3.6 + 1/3.7)
    assert opp.is_arb


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        find_arbitrage([2.0])         # need >= 2
    with pytest.raises(ValueError):
        find_arbitrage([1.0, 2.0])    # odds must be > 1
