from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Explanation:
    source: str
    target: str
    explanation: str
    confidence: float

    # NEW (important for production)
    components: List[str] = None
    evidence: Dict = None