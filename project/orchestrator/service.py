import logging
import uuid

from orchestrator.executor import LevelExecutor


logger = logging.getLogger(__name__)


class RecomputeOrchestrator:

    def __init__(self):
        self.executor = LevelExecutor()

    def run(self, impact_result):

        execution_id = str(uuid.uuid4())

        levels = impact_result.levels

        final_results = {}

        logger.info(
            "recompute_started",
            extra={
                "execution_id": execution_id
            }
        )

        for level in sorted(levels.keys()):

            logger.info(
                "level_started",
                extra={
                    "execution_id": execution_id,
                    "level": level,
                }
            )

            nodes = levels[level]

            results = self.executor.execute_level(
                execution_id,
                nodes
            )

            final_results[level] = results

            logger.info(
                "level_completed",
                extra={
                    "execution_id": execution_id,
                    "level": level,
                    "node_count": len(nodes),
                }
            )

        logger.info(
            "recompute_completed",
            extra={
                "execution_id": execution_id
            }
        )

        return final_results