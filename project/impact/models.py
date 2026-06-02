from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ImpactResult:
    """
    Immutable result of graph impact analysis.

    Attributes:
        seed_nodes:
            Nodes directly changed in GraphDiff.

        impacted_nodes:
            All impacted nodes including seeds.

        levels:
            Impact expansion grouped by traversal depth.

            Example:
            {
                0: ("A",),
                1: ("B", "C"),
                2: ("D",)
            }
    """

    seed_nodes: tuple[str, ...]
    impacted_nodes: tuple[str, ...]
    levels: Mapping[int, tuple[str, ...]]

    @property
    def total_impacted(self) -> int:
        return len(self.impacted_nodes)

    def is_empty(self) -> bool:
        return not self.impacted_nodes