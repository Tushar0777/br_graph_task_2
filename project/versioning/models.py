from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, UTC

from graph.models import Graph


@dataclass(frozen=True)
class GraphVersion:
    version_id: int
    created_at: datetime
    graph: Graph

    def __post_init__(self):
        if self.version_id <= 0:
            raise ValueError(
                "version_id must be positive"
            )

        if self.graph is None:
            raise ValueError(
                "graph cannot be None"
            )

    @classmethod
    def create(
        cls,
        version_id: int,
        graph: Graph
    ) -> "GraphVersion":
        return cls(
            version_id=version_id,
            created_at=datetime.now(UTC),
            graph=deepcopy(graph)
        )