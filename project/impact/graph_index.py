from collections import defaultdict
from dataclasses import dataclass
from typing import Mapping

from graph.models import Graph


_EMPTY_DEPENDENTS: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GraphIndex:
    """
    Optimized adjacency index for graph traversal.

    Stores precomputed graph relationships to support
    efficient impact propagation.

    Direction:
        A -> B means B depends on A

    Therefore:
        change(A) impacts B
    """

    forward_adj: Mapping[str, tuple[str, ...]]
    reverse_adj: Mapping[str, tuple[str, ...]]

    @classmethod
    def build(cls, graph: Graph) -> "GraphIndex":
        """
        Build immutable adjacency indexes.

        Complexity:
            O(E)
        """

        forward: dict[str, list[str]] = defaultdict(list)
        reverse: dict[str, list[str]] = defaultdict(list)

        for edge in graph.edges:
            forward[edge.source].append(edge.target)
            reverse[edge.target].append(edge.source)

        return cls(
            forward_adj={
                node: tuple(sorted(targets))
                for node, targets in forward.items()
            },
            reverse_adj={
                node: tuple(sorted(sources))
                for node, sources in reverse.items()
            },
        )

    def get_dependents(self, node_id: str) -> tuple[str, ...]:
        """
        Get nodes impacted by node changes.

        Example:
            A -> B

            get_dependents(A)
            returns ("B",)
        """
        return self.forward_adj.get(
            node_id,
            _EMPTY_DEPENDENTS,
        )

    def get_dependencies(self, node_id: str) -> tuple[str, ...]:
        """
        Get upstream dependencies.

        Example:
            A -> B

            get_dependencies(B)
            returns ("A",)
        """
        return self.reverse_adj.get(
            node_id,
            _EMPTY_DEPENDENTS,
        )