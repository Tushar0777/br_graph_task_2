from graph.models import Graph, Node, Edge
from diff.models import GraphDiff
from impact.service import ImpactAnalysisService
from impact.traversal import BFSTraversal


def main():

    graph = Graph(
        nodes=[
            Node(id="A"),
            Node(id="B"),
            Node(id="C"),
            Node(id="D")
        ],
        edges=[
            Edge(source="A", target="B"),
            Edge(source="B", target="C"),
            Edge(source="C", target="D"),
        ]
    )

    diff = GraphDiff(
        added_nodes=[],
        removed_nodes=[],
        updated_nodes=[Node(id="A")],
        added_edges=[],
        removed_edges=[]
    )

    service = ImpactAnalysisService(
        traversal_strategy=BFSTraversal()
    )

    result = service.analyze(graph, diff)

    print("\nImpacted Nodes:")
    print(result.impacted_nodes)

    print("\nLevels:")
    print(result.levels)


if __name__ == "__main__":
    main()