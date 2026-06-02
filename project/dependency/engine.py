class DependencyEngine:

    def __init__(self):
        self.candidate_gen = CandidateGenerator()
        self.feature_eng = FeatureEngineer()
        self.embedding = EmbeddingService()
        self.store = OpenSearchVectorStore()
        self.llm = LLMDependencyDecider()

    def build(self, rules):

        edges = []

        # Step 1: Index embeddings (OK, but should be separate pipeline)
        for rule in rules:
            vec = self.embedding.encode(rule.text)
            self.store.index_rule(rule.id, vec)

        # Step 2: Candidate generation
        candidates = self.candidate_gen.generate(rules)

        # Step 3: Evaluate candidates
        for r1, r2 in candidates:

            features = self.feature_eng.compute(r1, r2)

            score = self._heuristic_score(features)

            if score > 0.85:
                decision, llm_score = True, score

            elif score < 0.3:
                decision, llm_score = False, score

            else:
                decision, llm_score = self.llm.decide(r1, r2, features)

            if decision:
                edges.append(
                    DependencyEdge(
                        source=r1.id,
                        target=r2.id,
                        confidence=llm_score
                    )
                )

        return edges

    def _heuristic_score(self, f):
        return (
            0.4 * (f["attr_overlap"] > 0) +
            0.4 * (f["text_sim"] > 0.2) +
            0.2 * (f["seq_distance"] < 3)
        )