
"""Road-closure and road-widening what-if experiments."""

from collections.abc import Callable
from operator import index
from typing import Protocol

from evac.network import FlowNetwork, Node


class FlowResult(Protocol):
    """Result containing a maximum-flow value."""

    value: int


Solver = Callable[[FlowNetwork, Node, Node], FlowResult]


def closure_losses(
    network: FlowNetwork,
    s: Node,
    t: Node,
    solver: Solver,
) -> dict[int, int]:
    """Return the maximum-flow loss when each directed road closes.

    Each road is tested independently on a copy of the original network.
    The original network and its flow remain unchanged.
    """

    baseline_network = network.copy()
    baseline_network.reset_flow()
    baseline = solver(baseline_network, s, t).value

    losses: dict[int, int] = {}

    for edge in network.roads():
        modified = network.copy()
        modified.reset_flow()
        modified.set_capacity(edge, 0)

        new_flow = solver(modified, s, t).value
        losses[edge] = baseline - new_flow

    return losses


def widening_gains(
    network: FlowNetwork,
    s: Node,
    t: Node,
    solver: Solver,
    added_capacity: int,
) -> dict[int, int]:
    """Return the maximum-flow gain when each directed road is widened.

    Each road receives the same additional capacity independently.
    The original network and its flow remain unchanged.
    """

    if isinstance(added_capacity, bool):
        raise ValueError("added_capacity must be a nonnegative integer")

    try:
        added_capacity = index(added_capacity)
    except TypeError as exc:
        raise ValueError(
            "added_capacity must be a nonnegative integer"
        ) from exc

    if added_capacity < 0:
        raise ValueError("added_capacity must be a nonnegative integer")

    baseline_network = network.copy()
    baseline_network.reset_flow()
    baseline = solver(baseline_network, s, t).value

    gains: dict[int, int] = {}

    for edge in network.roads():
        modified = network.copy()
        modified.reset_flow()

        new_capacity = modified.capacity(edge) + added_capacity
        modified.set_capacity(edge, new_capacity)

        new_flow = solver(modified, s, t).value
        gains[edge] = new_flow - baseline

    return gains
