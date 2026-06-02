from dataclasses import dataclass, field
from typing import Tuple

from graph.models import Node, Edge


@dataclass(frozen=True)
class NodeUpdate:
    old: Node
    new: Node


@dataclass(frozen=True)
class GraphDiff:
    added_nodes: tuple[Node, ...] = ()
    removed_nodes: tuple[Node, ...] = ()
    updated_nodes: tuple[NodeUpdate, ...] = ()

    added_edges: tuple[Edge, ...] = ()
    removed_edges: tuple[Edge, ...] = ()

    from_version: int | None = None
    to_version: int | None = None

    @property
    def has_changes(self) -> bool:
        return self.total_changes > 0

    @property
    def total_changes(self) -> int:
        return (
            len(self.added_nodes)
            + len(self.removed_nodes)
            + len(self.updated_nodes)
            + len(self.added_edges)
            + len(self.removed_edges)
        )