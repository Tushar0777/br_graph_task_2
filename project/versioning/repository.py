from copy import deepcopy
from datetime import datetime, UTC
from threading import Lock
from typing import Optional

from graph.models import Graph, Node, Edge
from versioning.models import GraphVersion


class VersionNotFoundError(Exception):
    pass


class InvalidGraphDataError(Exception):
    pass


class VersionRepository:
    """
    In-memory repository.

    Replace with PostgreSQL
    in production.
    """

    def __init__(self):

        self.storage: dict[int, dict] = {}

        self.next_version_id = 1

        self.latest_version_id: Optional[int] = None

        self.lock = Lock()

    def save(
        self,
        graph: Graph
    ) -> GraphVersion:
        """
        Save immutable graph snapshot.
        """

        with self.lock:

            version_id = self.next_version_id
            self.next_version_id += 1

        graph_copy = deepcopy(graph)

        created_at = datetime.now(UTC)

        record = {
            "version_id": version_id,
            "created_at": created_at,
            "graph": self._serialize_graph(
                graph_copy
            )
        }

        self.storage[version_id] = record
        self.latest_version_id = version_id

        return GraphVersion(
            version_id=version_id,
            created_at=created_at,
            graph=graph_copy
        )

    def get_latest(
        self
    ) -> Optional[GraphVersion]:

        if self.latest_version_id is None:
            return None

        return self.get_by_version(
            self.latest_version_id
        )

    def get_by_version(
        self,
        version_id: int
    ) -> GraphVersion:

        record = self.storage.get(
            version_id
        )

        if record is None:
            raise VersionNotFoundError(
                f"Version {version_id} not found"
            )

        graph = self._deserialize_graph(
            record["graph"]
        )

        return GraphVersion(
            version_id=record["version_id"],
            created_at=record["created_at"],
            graph=graph
        )



    def list_versions(self) -> list[int]:

        return sorted(
            self.storage.keys()
        )
    


    def delete_version(
        self,
        version_id: int
    ) -> None:

        if version_id not in self.storage:
            raise VersionNotFoundError(
                f"Version {version_id} not found"
            )

        del self.storage[version_id]

        if version_id == self.latest_version_id:

            self.latest_version_id = (
                max(self.storage.keys())
                if self.storage
                else None
            )

    # -------------------------
    # Serialization
    # -------------------------

    def _serialize_graph(
        self,
        graph: Graph
    ) -> dict:
        '''
         Convert Graph to dict for storage.'''

        return {
            "nodes": [
                node.__dict__
                for node in graph.nodes
            ],
            "edges": [
                edge.__dict__
                for edge in graph.edges
            ]
        }

    def _deserialize_graph(
        self,
        data: dict
    ) -> Graph:
        ''' Convert dict back to Graph.'''

        try:
            nodes = [
                Node(**node)
                for node in data.get(
                    "nodes", []
                )
            ]

            edges = [
                Edge(**edge)
                for edge in data.get(
                    "edges", []
                )
            ]

            return Graph(
                nodes=nodes,
                edges=edges
            )

        except Exception as e:
            raise InvalidGraphDataError(
                "Corrupted graph data"
            ) from e