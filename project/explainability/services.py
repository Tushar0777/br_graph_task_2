from explainability.builder import ExplanationBuilder
from explainability.llm_enhancer import LLMEnhancer
from explainability.models import Explanation


class ExplainabilityService:

    def __init__(self, use_llm=True):
        self.builder = ExplanationBuilder()
        self.llm = LLMEnhancer()
        self.use_llm = use_llm

    def explain(self, r1, r2, features, confidence):

        base_explanations, components = self.builder.build(r1, r2, features)

        evidence = {
            "rule_a_attributes": list(getattr(r1, "attributes", [])),
            "rule_b_attributes": list(getattr(r2, "attributes", [])),
            "shared_attributes": list(
                set(r1.attributes) & set(r2.attributes)
            )
        }

        if self.use_llm:
            llm_output = self.llm.enhance(r1, r2, base_explanations)
            final_text = llm_output["final_explanation"]
        else:
            final_text = " | ".join(base_explanations)

        return Explanation(
            source=r1.id,
            target=r2.id,
            explanation=final_text,
            confidence=max(0.0, min(confidence, 1.0)),
            components=components,
            evidence=evidence
        )