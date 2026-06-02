from collections import defaultdict, deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from impact.graph_index import GraphIndex


@dataclass(frozen=True, slots=True)
class TraversalNode:
    node_id: str
    level: int


class BFSTraversal:
    """
    Multi-source BFS traversal for impact propagation.

    Traverses graph dependents level-by-level.

    Example:
        A -> B -> D
        A -> C

    Output:
        {
            0: ("A",),
            1: ("B", "C"),
            2: ("D",)
        }

    Complexity:
        O(N + E)
    """

    def traverse(
        self,
        seeds: Iterable[str],
        graph_index: GraphIndex,
    ) -> Mapping[int, tuple[str, ...]]:

        unique_seeds = tuple(sorted(set(seeds)))

        if not unique_seeds:
            return {}

        visited: set[str] = set(unique_seeds)

        queue: deque[TraversalNode] = deque(
            TraversalNode(node_id=s, level=0)
            for s in unique_seeds
        )

        levels: dict[int, list[str]] = defaultdict(list)

        while queue:
            current = queue.popleft()

            levels[current.level].append(
                current.node_id
            )

            for dependent in graph_index.get_dependents(
                current.node_id
            ):
                if dependent in visited:
                    continue

                visited.add(dependent)

                queue.append(
                    TraversalNode(
                        node_id=dependent,
                        level=current.level + 1,
                    )
                )

        return {
            level: tuple(nodes)
            for level, nodes in sorted(levels.items())
        }