class ExplanationTemplates:

    def attribute_overlap(self, attrs):
        return f"Both rules share common attributes: {', '.join(attrs)}"

    def sequence(self, r1, r2):
        return f"Rule {r1.id} occurs before Rule {r2.id} in the journey"

    def text_similarity(self):
        return "Both rules have similar textual patterns"

    def logical_flow(self, attrs):
        return f"Rule A produces values ({', '.join(attrs)}) used in Rule B"