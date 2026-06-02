from collections.abc import Iterable
from dataclasses import dataclass

from graph.models import Edge
from diff.utils import (
    build_edge_signature_set,
    edge_signature,
)


@dataclass(frozen=True)
class EdgeDiffResult:
    added: tuple[Edge, ...]
    removed: tuple[Edge, ...]


class EdgeDiffer:
    """
    Compute edge-level graph diff.

    Detects:
    - added edges
    - removed edges

    Complexity:
        O(E)
    """

    def diff(
        self,
        old_edges: Iterable[Edge],
        new_edges: Iterable[Edge],
    ) -> EdgeDiffResult:

        old_set = build_edge_signature_set(old_edges)
        new_set = build_edge_signature_set(new_edges)

        added = [
            edge
            for edge in new_edges
            if edge_signature(edge)
            not in old_set
        ]

        removed = [
            edge
            for edge in old_edges
            if edge_signature(edge)
            not in new_set
        ]

        return EdgeDiffResult(
            added=tuple(
                sorted(
                    added,
                    key=lambda e: (
                        e.source,
                        e.target,
                        e.type,
                    ),
                )
            ),
            removed=tuple(
                sorted(
                    removed,
                    key=lambda e: (
                        e.source,
                        e.target,
                        e.type,
                    ),
                )
            ),
        )