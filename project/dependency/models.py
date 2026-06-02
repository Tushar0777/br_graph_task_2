from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Rule:
    id: str
    text: str
    attributes: dict[str, Any]
    journey: str
    sequence: int


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str
    confidence: float

    # production additions
    reason: str | None = None
    source_type: str | None = None  # llm / embedding / heuristic


@dataclass
class FeatureVector:
    attr_overlap: float
    seq_distance: float
    text_sim: float
    embedding_sim: float | None