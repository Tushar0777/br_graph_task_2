from explainability.templates import ExplanationTemplates


class ExplanationBuilder:

    def __init__(self):
        self.templates = ExplanationTemplates()

    def build(self, r1, r2, features):

        explanations = []
        components = []

        overlap = set(r1.attributes) & set(r2.attributes)

        # Attribute overlap
        if overlap:
            explanations.append(
                self.templates.attribute_overlap(overlap)
            )
            components.append("attribute_overlap")

        # Sequence logic
        if r1.sequence < r2.sequence:
            explanations.append(
                self.templates.sequence(r1, r2)
            )
            components.append("sequence")

        # Text similarity
        text_sim = features.get("text_sim", 0.0)
        if text_sim > 0.2:
            explanations.append(
                self.templates.text_similarity()
            )
            components.append("text_similarity")

        # Logical flow
        if overlap:
            explanations.append(
                self.templates.logical_flow(overlap)
            )
            components.append("logical_flow")

        return explanations, components