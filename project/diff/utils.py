from collections.abc import Iterable

from graph.models import (
    Node,
    Edge,
)


def build_node_index(
    nodes: Iterable[Node],
) -> dict[str, Node]:

    index = {}

    for node in nodes:
        if node.id in index:
            raise ValueError(
                f"Duplicate node id: {node.id}"
            )

        index[node.id] = node

    return index


def edge_signature(
    edge: Edge,
) -> tuple[str, str, str]:
    """
    Create hashable edge identity.
    """

    return (
        edge.source,
        edge.target,
        edge.type,
    )


def build_edge_signature_set(
    edges: Iterable[Edge],
) -> set[tuple[str, str, str]]:
    """
    Build hashable edge lookup set.
    """

    return {
        edge_signature(edge)
        for edge in edges
    }