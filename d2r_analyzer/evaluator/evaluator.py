import json
import logging

from d2r_analyzer.evaluator.manual_evaluation import ManualEvaluator
from d2r_analyzer.llm.client import LLMClient
from d2r_analyzer.llm.parser import (
    EvaluationSchema,
    ItemSchema,
    parse_evaluation,
    parse_item,
)

logger = logging.getLogger(__name__)


def correct_quality(item: dict) -> dict:

    affixes = item.get("affixes", [])
    name = (item.get("name") or "").lower().strip()
    affix_count = len(affixes)

    if affix_count <= 2 and item.get("quality") in ("rare", "unique", "set"):
        item["quality"] = "magic"

    if affix_count >= 3 and item.get("quality") == "magic":
        item["quality"] = "rare"

    words = name.split()
    if len(words) == 2 and item.get("quality") == "magic":
        item["quality"] = "rare"

    return item


class Evaluator:
    def __init__(
        self,
        llm_model: str,
        llm_base_url: str,
        llm_api_key: str,
        evaluation_mode: str,
        manual_rules_file: str = None,
    ) -> None:
        self.evaluation_mode = evaluation_mode
        self.llm = LLMClient(
            model_name=llm_model, base_url=llm_base_url, api_key=llm_api_key
        )
        if self.evaluation_mode == "manual":
            if not manual_rules_file:
                raise ValueError("Manual evaluation mode requires a rules file")
            with open(manual_rules_file, "r") as f:
                manual_rules = json.load(f)
            self.manual_evaluator = ManualEvaluator(manual_rules)

    def parse_item(self, image_base64: str) -> ItemSchema:
        raw = self.llm.extract_item_info(image_base64)
        parsed = parse_item(raw)
        corrected = correct_quality(parsed.model_dump())
        return parse_item(corrected)

    def evaluate_item(self, item: ItemSchema) -> EvaluationSchema:
        if self.evaluation_mode == "manual":
            logger.debug("Manual evaluation mode — skipping LLM evaluation")
            evaluation = self.manual_evaluator.evaluate_item(item.model_dump())
            return EvaluationSchema(
                grade=evaluation.get("grade", "C"),
                verdict=evaluation.get("verdict", ""),
                best_build="",
                trade_value="",
                reasoning="",
                good_affixes=evaluation.get("good_affixes", []),
                wasted_slots=[],
                roll_quality="",
            )
        elif self.evaluation_mode == "llm":
            raw = self.llm.evaluate_item(item.model_dump_json())
            return parse_evaluation(raw)
        else:
            raise ValueError(f"Unknown evaluation mode: {self.evaluation_mode}")
