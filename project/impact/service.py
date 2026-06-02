from collections.abc import Iterable
from typing import Protocol

from diff.models import GraphDiff
from graph.models import Graph
from impact.graph_index import GraphIndex
from impact.models import ImpactResult


class TraversalStrategy(Protocol):

    def traverse(
        self,
        seeds: Iterable[str],
        graph_index: GraphIndex,
    ) -> dict[int, tuple[str, ...]]:
        ...


class ImpactAnalysisService:
    """
    Determines graph impact from GraphDiff.

    Workflow:
        1. Extract changed nodes
        2. Build graph index
        3. Traverse dependents
        4. Build immutable result
    """

    def __init__(
        self,
        traversal_strategy: TraversalStrategy,
    ) -> None:
        self._traversal = traversal_strategy

    def analyze(
        self,
        graph: Graph,
        diff: GraphDiff,
    ) -> ImpactResult:

        seed_nodes = self._extract_seed_nodes(diff)

        if not seed_nodes:
            return ImpactResult(
                seed_nodes=(),
                impacted_nodes=(),
                levels={},
            )

        graph_index = GraphIndex.build(graph)

        levels = self._traversal.traverse(
            seeds=seed_nodes,
            graph_index=graph_index,
        )

        impacted_nodes = tuple(
            node
            for level_nodes in levels.values()
            for node in level_nodes
        )

        return ImpactResult(
            seed_nodes=seed_nodes,
            impacted_nodes=impacted_nodes,
            levels=levels,
        )

    @staticmethod
    def _extract_seed_nodes(
        diff: GraphDiff,
    ) -> tuple[str, ...]:

        seeds = {
            node.id
            for node in (
                list(diff.added_nodes)
                + list(diff.updated_nodes)
                + list(diff.removed_nodes)
            )
        }

        return tuple(sorted(seeds))