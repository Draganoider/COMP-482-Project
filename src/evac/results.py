"""Results shared by the two max-flow algorithms.

`MaxFlowResult` is what MaxFlow in analysis/max-flow.md section 2 returns: the flow, its value and
the counters `paths` (here `augmenting_paths`) and `scanned` (here `edges_scanned`) that
experiment E1 reads.
"""

from dataclasses import dataclass


@dataclass
class MaxFlowResult:
    """Maximum flow and the work used to find it.

    ``flow`` is a snapshot keyed by the network's forward edge IDs. It includes
    super-terminal edges, if present; parallel roads have separate entries.
    ``edges_scanned`` includes zero-residual edges and the final failed search.
    """

    value: int
    flow: dict[int, int]
    augmenting_paths: int
    edges_scanned: int
