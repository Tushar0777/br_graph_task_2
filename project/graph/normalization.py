from copy import deepcopy
import re
from graph.models import Graph, Node, Edge




class GraphNormalizer:
    '''Normalizes node IDs in a graph by converting them to lowercase, 
    replacing spaces with underscores, and removing special characters.
    This ensures consistency and helps avoid issues with ID matching.

    Example:

    Input Graph:

    Nodes:

    - id: "Node 1", type: "typeA"  
    - id: "Node-2", type: "typeB"

    Edges:

    - source: "Node 1", target: "Node-2", type: "depends_on"

    
    Output Graph:

    Nodes:

    - id: "node_1", type: "typeA"
    - id: "node_2", type: "typeB"

    Edges:

    - source: "node_1", target: "node_2", type: "depends_on"

    '''

    # def normalize_id(self, text: str) -> str:
    #     text = text.strip().lower()
    #     text = re.sub(r"\s+", "_", text)
    #     text = re.sub(r"[^a-z0-9_]", "", text)
    #     return text

    # def process(self, graph: Graph) -> Graph:
    #     normalized_nodes = []
    #     id_map = {}

    #     for node in graph.nodes:
    #         new_id = self.normalize_id(node.id)
    #         id_map[node.id] = new_id
    #         normalized_nodes.append(Node(id=new_id, type=node.type, metadata=node.metadata))

    #     normalized_edges = []
    #     for edge in graph.edges:
    #         normalized_edges.append(
    #             Edge(
    #                 source=id_map.get(edge.source, edge.source),
    #                 target=id_map.get(edge.target, edge.target),
    #                 type=edge.type
    #             )
    #         )

    #     return Graph(nodes=normalized_nodes, edges=normalized_edges)

    SPACE_PATTERN = re.compile(r"\s+")
    SPECIAL_PATTERN = re.compile(r"[^a-z0-9_]")

    def normalize_id(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Empty node id")

        text = text.strip().lower()
        text = self.SPACE_PATTERN.sub("_", text)
        text = self.SPECIAL_PATTERN.sub("", text)

        if not text:
            raise ValueError(
                "Invalid normalized id"
            )

        return text

    def process(self, graph: Graph) -> Graph:

        if graph is None:
            raise ValueError(
                "Graph cannot be None"
            )

        normalized_nodes = []
        normalized_edges = []
        id_map: dict[str, str] = {}

        for node in graph.nodes:

            new_id = self.normalize_id(node.id)

            id_map[node.id] = new_id

            normalized_nodes.append(
                Node(
                    id=new_id,
                    type=node.type,
                    metadata=node.metadata
                )
            )

        for edge in graph.edges:

            normalized_edges.append(
                Edge(
                    source=id_map.get(
                        edge.source,
                        edge.source
                    ),
                    target=id_map.get(
                        edge.target,
                        edge.target
                    ),
                    type=edge.type
                )
            )

        return Graph(
            nodes=normalized_nodes,
            edges=normalized_edges
        )