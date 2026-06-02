from graph.models import Graph, Node, Edge


# class GraphDeduplicator:

#     def process(self, graph: Graph) -> Graph:
#         unique_nodes = {}
        
#         for node in graph.nodes:
#             if node.id not in unique_nodes:
#                 unique_nodes[node.id] = node

#         dedup_nodes = list(unique_nodes.values())

#         valid_ids = set(unique_nodes.keys())

#         dedup_edges = []
#         for edge in graph.edges:
#             if edge.source in valid_ids and edge.target in valid_ids:
#                 dedup_edges.append(edge)

#         return Graph(nodes=dedup_nodes, edges=dedup_edges)

from copy import deepcopy

from graph.models import Graph, Node, Edge


class GraphDeduplicator:

    def process(self, graph: Graph) -> Graph:

        if graph is None:
            raise ValueError("Graph cannot be None")

        unique_nodes: dict[str, Node] = {}

        for node in graph.nodes:

            existing = unique_nodes.get(node.id)

            if existing:

                if (existing.type != node.type
                    or existing.metadata != node.metadata):
                    
                    raise ValueError(
                        f"Conflicting duplicate node: "
                        f"{node.id}"
                    )

                continue

            unique_nodes[node.id] = deepcopy(node)

        valid_ids = set(unique_nodes.keys())

        dedup_edges: list[Edge] = []
        seen_edges: set[tuple] = set()

        for edge in graph.edges:

            if (
                edge.source not in valid_ids
                or edge.target not in valid_ids
            ):
                continue

            edge_key = (
                edge.source,
                edge.target,
                edge.type
            )

            if edge_key in seen_edges:
                continue

            seen_edges.add(edge_key)

            dedup_edges.append(
                deepcopy(edge)
            )

        return Graph(
            nodes=list(unique_nodes.values()),
            edges=dedup_edges
        )