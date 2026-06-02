from typing import Optional

from graph.models import Graph
from versioning.models import GraphVersion
from versioning.repository import VersionRepository


class VersionManager:

    def __init__(self,repo: VersionRepository):
        self.repo = repo

    def create_version(self,graph: Graph) -> GraphVersion:
        return self.repo.save(graph)
    


    def get_latest(self) -> Optional[GraphVersion]:
        return self.repo.get_latest()


    def get_version(self,version_id: int) -> Optional[GraphVersion]:
        return self.repo.get_by_version(
            version_id
        )
    


    def get_diff_input (self,new_graph: Graph) -> tuple[Optional[Graph],Graph]:

        latest = self.repo.get_latest()

        old_graph = (
            latest.graph
            if latest
            else None
)

        return (old_graph,new_graph)


    def rollback(self,version_id: int) -> GraphVersion:

        version = (self.repo.get_by_version(version_id))

        return self.repo.save(version.graph)