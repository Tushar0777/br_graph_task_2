from collections.abc import Iterable
from dataclasses import dataclass

from graph.models import Node
from diff.utils import build_node_index


@dataclass(frozen=True)
class NodeUpdate:
    old: Node
    new: Node


@dataclass(frozen=True)
class NodeDiffResult:
    added: tuple[Node, ...]
    removed: tuple[Node, ...]
    updated: tuple[NodeUpdate, ...]


class NodeDiffer:
    """
    Compute node-level graph diff.

    Detects:
    - added nodes
    - removed nodes
    - updated nodes

    Complexity:
        O(N)
    """

    def diff(
        self,
        old_nodes: Iterable[Node],
        new_nodes: Iterable[Node],
    ) -> NodeDiffResult:

        old_map = build_node_index(old_nodes)
        new_map = build_node_index(new_nodes)

        added: list[Node] = []
        removed: list[Node] = []
        updated: list[NodeUpdate] = []

        for node_id, new_node in new_map.items():

            old_node = old_map.get(node_id)

            if old_node is None:
                added.append(new_node)
                continue

            if (old_node.type != new_node.type or old_node.metadata != new_node.metadata):
                updated.append(
                    NodeUpdate(
                        old=old_node,
                        new=new_node,
                    )
                )

        for node_id, old_node in old_map.items():
            if node_id not in new_map:
                removed.append(old_node)

        return NodeDiffResult(
            added=tuple(
                sorted(
                    added,
                    key=lambda n: n.id
                )
            ),
            removed=tuple(
                sorted(
                    removed,
                    key=lambda n: n.id
                )
            ),
            updated=tuple(
                sorted(
                    updated,
                    key=lambda n: n.new.id
                )
            ),
        )