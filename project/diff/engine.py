from graph.models import Graph
from diff.node_diff import NodeDiffer
from diff.edge_diff import EdgeDiffer
from diff.models import GraphDiff


class GraphDiffEngine:
    """
    Compute graph-level diff between
    two graph versions.

    Detects:
    - added nodes
    - removed nodes
    - updated nodes
    - added edges
    - removed edges

    Complexity:
        O(N + E)
    """

    def __init__(
        self,
        node_differ: NodeDiffer,
        edge_differ: EdgeDiffer,
    ) -> None:
        self.node_differ = node_differ
        self.edge_differ = edge_differ

    def diff(
        self,
        old_graph: Graph | None,
        new_graph: Graph,
    ) -> GraphDiff:

        if new_graph is None:
            raise ValueError(
                "new_graph cannot be None."
            )

        if old_graph is None:
            return GraphDiff(
                added_nodes=tuple(
                    sorted(
                        new_graph.nodes,
                        key=lambda n: n.id
                    )
                ),
                removed_nodes=(),
                updated_nodes=(),
                added_edges=tuple(
                    sorted(
                        new_graph.edges,
                        key=lambda e: (
                            e.source,
                            e.target,
                            e.type,
                        )
                    )
                ),
                removed_edges=(),
            )

        node_diff = self.node_differ.diff(
            old_graph.nodes,
            new_graph.nodes,
        )

        edge_diff = self.edge_differ.diff(
            old_graph.edges,
            new_graph.edges,
        )

        return GraphDiff(
            added_nodes=node_diff.added,
            removed_nodes=node_diff.removed,
            updated_nodes=node_diff.updated,
            added_edges=edge_diff.added,
            removed_edges=edge_diff.removed,
        )