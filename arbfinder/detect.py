"""Arbitrage detection across mutually-exclusive outcomes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ArbOpportunity:
    """A detected arbitrage.

    `odds` are the best decimal odds per outcome (one bookmaker each).
    `arb_percent` is the guaranteed return on total stake (e.g. 0.018 = 1.8%).
    `implied` is the sum of 1/odds (the 'arb book'); < 1 means an arb.
    """
    odds: list[float]
    implied: float
    arb_percent: float

    @property
    def is_arb(self) -> bool:
        return self.implied < 1.0


def find_arbitrage(odds: list[float]) -> ArbOpportunity:
    """Check a set of best-per-outcome decimal odds for an arbitrage.

    For mutually-exclusive, collectively-exhaustive outcomes, an arb
    exists iff sum(1/d_i) < 1. The guaranteed return on total stake is
    1 / sum(1/d_i) - 1.
    """
    if len(odds) < 2:
        raise ValueError("need at least 2 outcomes")
    if any(o <= 1.0 for o in odds):
        raise ValueError("all decimal odds must be > 1")
    implied = sum(1.0 / o for o in odds)
    arb_percent = (1.0 / implied) - 1.0
    return ArbOpportunity(odds=list(odds), implied=implied,
                          arb_percent=arb_percent)
