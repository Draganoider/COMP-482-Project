
"""Shared result structure for maximum-flow algorithms."""

from dataclasses import dataclass


@dataclass
class MaxFlowResult:
    """Store the maximum-flow value and algorithm counters."""

    value: int
    paths: int
    scanned: int
