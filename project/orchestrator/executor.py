from celery import group
from orchestrator.tasks import recompute_node


class LevelExecutor:

    def execute_level(
        self,
        execution_id: str,
        nodes: list[str]
    ):

        ordered_nodes = sorted(nodes)

        tasks = [
            recompute_node.s(
                execution_id,
                node_id
            )
            for node_id in ordered_nodes
        ]

        job = group(tasks)

        result = job.apply_async()

        return result.get(timeout=300)