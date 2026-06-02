import time

from impact.models import ImpactResult
from orchestrator.service import (
    RecomputeOrchestrator,
)


def main():

    impact = ImpactResult(
        seed_nodes=["A"],
        impacted_nodes=["A", "B", "C", "D"],
        levels={
            0: ["A"],
            1: ["B", "C"],
            2: ["D"]
        }
    )

    orchestrator = RecomputeOrchestrator()

    try:
        start = time.perf_counter()

        results = orchestrator.run(impact)

        duration = time.perf_counter() - start

        print("\nFinal Results:")
        print(results)

        print(
            f"\nExecution completed "
            f"in {duration:.2f}s"
        )

    except Exception as exc:
        print(
            f"Recompute failed: {exc}"
        )


if __name__ == "__main__":
    main()