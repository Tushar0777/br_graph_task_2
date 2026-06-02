class LLMDependencyDecider:

    def decide(self, r1, r2, features):

        contributions = {}

        contributions["attr"] = 0.4 if features["attr_overlap"] > 0 else 0.0
        contributions["text"] = 0.4 if features["text_sim"] > 0.2 else 0.0
        contributions["seq"] = 0.2 if features["seq_distance"] < 3 else 0.0

        score = sum(contributions.values())

        return {
            "is_dependent": score > 0.6,
            "score": score,
            "contributions": contributions
        }