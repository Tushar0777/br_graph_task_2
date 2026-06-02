from typing import Iterable, Tuple, Iterator
from dependency.models import Rule


class CandidateGenerator:

    def generate(self, rules: list[Rule]) -> Iterator[tuple[Rule, Rule]]:

        # Step 1: pre-group by journey (critical optimization)
        journey_map: dict[str, list[Rule]] = {}

        for r in rules:
            journey_map.setdefault(r.journey, []).append(r)

        # Step 2: only compare within journey
        for journey_rules in journey_map.values():

            # optional: sort by sequence
            journey_rules.sort(key=lambda x: x.sequence)

            n = len(journey_rules)

            for i in range(n):
                r1 = journey_rules[i]

                for j in range(i + 1, n):
                    r2 = journey_rules[j]

                    # sequence constraint already enforced by sorting
                    overlap = r1.attributes.keys() & r2.attributes.keys()

                    if not overlap:
                        continue

                    yield r1, r2