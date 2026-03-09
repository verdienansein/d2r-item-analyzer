try:
    from d2r_analyzer.llm.client import LLMClient
    from d2r_analyzer.llm.parser import (
        EvaluationSchema,
        ItemSchema,
        parse_evaluation,
        parse_item,
    )
except ModuleNotFoundError:
    from llm.client import LLMClient
    from llm.parser import EvaluationSchema, ItemSchema, parse_evaluation, parse_item


class Evaluator:
    def __init__(self, llm_model, llm_base_url, llm_api_key, evaluation_mode):
        self.evaluation_mode = evaluation_mode
        self.llm = LLMClient(
            model_name=llm_model, base_url=llm_base_url, api_key=llm_api_key
        )

    def parse_item(self, image_base64: str) -> ItemSchema:
        raw = self.llm.extract_item_info(image_base64)
        return parse_item(raw)

    def evaluate_item(self, item: ItemSchema) -> EvaluationSchema:
        if self.evaluation_mode == "manual":
            print("Manual evaluation mode - skipping LLM evaluation")
            return EvaluationSchema(
                grade="",
                verdict="",
                best_build="",
                trade_value="",
                reasoning="",
                good_affixes=[],
                wasted_slots=[],
                roll_quality="",
            )
        elif self.evaluation_mode == "llm":
            raw = self.llm.evaluate_item(item.model_dump_json())
            return parse_evaluation(raw)
        else:
            raise ValueError(f"Unknown evaluation mode: {self.evaluation_mode}")
