class LLMEnhancer:

    def enhance(self, r1, r2, explanations):

        base = " | ".join(explanations)

        return {
            "final_explanation": (
                f"Rule {r2.id} depends on Rule {r1.id}: {base}"
            ),
            "llm_used": True
        }