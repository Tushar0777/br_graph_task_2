from graph.models import Graph


class GraphValidator:

    def process(self, graph: Graph) -> Graph:

        if graph is None:
            raise ValueError(
                "Graph cannot be None"
            )

        errors = []

        node_ids = set()
        duplicate_ids = set()

        for node in graph.nodes:

            if not node.id.strip():
                errors.append(
                    "Empty node id found"
                )
                continue

            if node.id in node_ids:
                duplicate_ids.add(
                    node.id
                )

            node_ids.add(node.id)

        if duplicate_ids:
            errors.append(
                f"Duplicate node ids: "
                f"{sorted(duplicate_ids)}"
            )

        for edge in graph.edges:

            if edge.source not in node_ids:
                errors.append(
                    f"Invalid edge source: "
                    f"{edge.source} "
                    f"(target={edge.target})"
                )

            if edge.target not in node_ids:
                errors.append(
                    f"Invalid edge target: "
                    f"{edge.target} "
                    f"(source={edge.source})"
                )

            if edge.source == edge.target:
                errors.append(
                    f"Self-loop edge: "
                    f"{edge.source}"
                )

        if errors:
            raise ValueError(errors)

        return graph