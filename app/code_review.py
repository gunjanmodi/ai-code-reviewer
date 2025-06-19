import json
import traceback
from abc import ABC

from app.guidelines import CATEGORY_GUIDELINES
from app.prompts.stage1 import STAGE_1_SCOPE_CLASSIFIER
from app.prompts.stage2 import STAGE_2_REVIEWER_TEMPLATE
from app.prompts.stage3 import STAGE_3_DEEP_DIVE


class CodeReviewerBase(ABC):

    def __init__(self, code: str):
        self.code = code

    def call_llm(self, prompt: str, max_tokens: int, response_format: str) -> str:
        raise NotImplementedError("Subclasses must implement call_llm method.")

    def execute(self):
        patch_text = self.code

        print("🧭 Stage 1: Classifying Code Scope...")
        categories = self.stage_1_scope_classification(patch_text)
        if not categories:
            return "No valid categories identified."

        print("🔍 Stage 2: Performing Targeted Review...")
        review = self.stage_2_targeted_review(patch_text, categories)
        with open("stage_2_review.md", "w", encoding="utf-8") as f:
            return f.write(review)

        print("\n🔐 Stage 3: Deep Dive Review (Security & Performance)...")
        deep_dive = self.stage_3_deep_dive(patch_text, ["Security / Auth", "Performance", "Edge Cases"])
        with open("stage_3_deep_dive.md", "w", encoding="utf-8") as f:
            return f.write(deep_dive)


    def stage_1_scope_classification(self, patch_text: str) -> list:

        prompt = STAGE_1_SCOPE_CLASSIFIER.format(patch=patch_text)
        result = self.call_llm(prompt, max_tokens=300, response_format="json_object")
        try:
            categories = json.loads(result)
            print(categories)
            return categories
        except Exception as e:
            print("Failed to parse categories. Raw output:\n", result)
            print("Error:", traceback.print_exc())
            return []

    def stage_2_targeted_review(self, patch: str, categories: list[str]) -> str:

        def _build_stage_2_prompt() -> str:
            guidelines = {}
            for cat in categories:
                if cat in CATEGORY_GUIDELINES:
                    guidelines[cat] = CATEGORY_GUIDELINES[cat]

            checklists = "\n".join(
                f"- **{cat}**: {guidelines[cat]}" for cat in guidelines
            )


            final_prompt = STAGE_2_REVIEWER_TEMPLATE.format(
                checklists=checklists,
                patch=patch
            )
            return final_prompt

        prompt = _build_stage_2_prompt()
        print(prompt)
        return self.call_llm(prompt, max_tokens=1200, response_format="text")


    def stage_3_deep_dive(self, patch: str, focus_areas: list[str]) -> str:
        if not focus_areas:
            return "Skipped deep dive.\n"
        prompt = STAGE_3_DEEP_DIVE.format(focus_areas=", ".join(focus_areas), patch=patch[:6000])
        return self.call_llm(prompt, max_tokens=1200, response_format="text")
