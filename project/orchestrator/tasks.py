import os
from celery import Celery
import time


broker_url = os.getenv(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0"
)

backend_url = os.getenv(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/0"
)


celery_app = Celery(
    "recompute",
    broker=broker_url,
    backend=backend_url,
)


@celery_app.task(bind=True, max_retries=3)
def recompute_node(
    self,
    execution_id: str,
    node_id: str,
):
    try:

        print(
            f"[{execution_id}] "
            f"Recomputing {node_id}"
        )

        time.sleep(1)

        return {
            "node": node_id,
            "result": f"computed_{node_id}"
        }

    except Exception as exc:
        raise self.retry(
            exc=exc,
            countdown=2
        )