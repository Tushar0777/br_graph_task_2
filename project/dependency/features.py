class FeatureEngineer:

    def compute(self, r1, r2):

        attr_overlap = len(
            set(r1.attributes.items()) & set(r2.attributes.items())
        )

        seq_distance = abs(r1.sequence - r2.sequence)

        text_sim = self.simple_text_similarity(r1.text, r2.text)

        return {
            "attr_overlap": attr_overlap,
            "seq_distance": seq_distance,
            "text_sim": text_sim
        }

    def simple_text_similarity(self, t1, t2):
        s1 = set(t1.lower().split())
        s2 = set(t2.lower().split())

        if not s1 or not s2:
            return 0.0

        return len(s1 & s2) / len(s1 | s2)