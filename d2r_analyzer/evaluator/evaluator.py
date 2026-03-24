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

_COLOR_TO_QUALITY: dict[str, str] = {
    "white": "normal",
    "grey": "normal",
    "gray": "normal",
    "blue": "magic",
    "yellow": "rare",
    "green": "set",
    "gold": "unique",
    "brown": "unique",
    "orange": "crafted",
}


def correct_quality(item: dict, known_unique_names: set[str] | None = None) -> dict:
    quality = item.get("quality", "")
    affixes = item.get("affixes", [])
    base_type = item.get("base_type", "")
    name = (item.get("name") or "").lower().strip()
    name_color = (item.get("name_color") or "").lower().strip()
    affix_count = len(affixes)

    color_quality = _COLOR_TO_QUALITY.get(name_color)

    if known_unique_names and name and name in known_unique_names:
        item["quality"] = "unique"
        return item

    if affix_count >= 3 and base_type not in (
        "small charm",
        "grand charm",
        "large charm",
    ):
        item["quality"] = "rare"
        return item

    if affix_count >= 1:
        item["quality"] = "magic"
        return item

    if quality in ("unique", "set"):
        return item
    if color_quality in ("unique", "set"):
        item["quality"] = color_quality
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
        known_uniques: set[str] | None = None
        if self.evaluation_mode == "manual" and hasattr(self, "manual_evaluator"):
            known_uniques = set(
                self.manual_evaluator.evaluation_rules.get("uniques", {}).keys()
            )
        corrected = correct_quality(parsed.model_dump(), known_uniques)
        return parse_item(corrected)

    def evaluate_item(self, item: ItemSchema) -> EvaluationSchema:
        if self.evaluation_mode == "manual":
            logger.debug("Manual evaluation mode — skipping LLM evaluation")
            evaluation = self.manual_evaluator.evaluate_item(item.model_dump())
            return EvaluationSchema(
                grade=evaluation.get("grade", "C"),
                verdict=evaluation.get("verdict", ""),
                reasoning=evaluation.get("reasoning", ""),
                good_affixes=[
                    a.get("raw_text", str(a)) if isinstance(a, dict) else str(a)
                    for a in evaluation.get("good_affixes", [])
                ],
                wasted_slots=[
                    a.get("raw_text", str(a)) if isinstance(a, dict) else str(a)
                    for a in evaluation.get("wasted_slots", [])
                ],
                roll_quality=str(evaluation.get("score", "")),
            )
        elif self.evaluation_mode == "llm":
            raw = self.llm.evaluate_item(item.model_dump_json())
            return parse_evaluation(raw)
        else:
            raise ValueError(f"Unknown evaluation mode: {self.evaluation_mode}")
