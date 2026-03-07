import os

try:
    from d2r_analyzer.llm.client import LLMClient
    from d2r_analyzer.llm.parser import ItemSchema, parse_item
except ModuleNotFoundError:
    from llm.client import LLMClient
    from llm.parser import ItemSchema, parse_item

llm_model = os.getenv("LLM_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
llm_base_url = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
llm_api_key = os.getenv("GROQ_API_KEY", "")


class Evaluator:
    def __init__(self):
        self.llm = LLMClient(
            model_name=llm_model, base_url=llm_base_url, api_key=llm_api_key
        )

    def parse_item(self, image_base64: str) -> ItemSchema:
        raw = self.llm.extract_item_info(image_base64)
        return parse_item(raw)
