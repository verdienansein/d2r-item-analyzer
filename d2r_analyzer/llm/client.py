from openai import OpenAI

from d2r_analyzer.llm.prompts import EVALUATION_PROMPT, ITEM_EXTRACTION_PROMPT


class LLMClient:
    def __init__(self, model_name: str, base_url: str, api_key: str) -> None:
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def extract_item_info(self, image_base64: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            max_tokens=1000,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ITEM_EXTRACTION_PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
        )
        raw = response.choices[0].message.content.strip()
        return raw

    def evaluate_item(self, item_json: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            max_tokens=1000,
            temperature=0.0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": EVALUATION_PROMPT.replace("{item_json}", item_json),
                        }
                    ],
                }
            ],
        )
        raw = response.choices[0].message.content.strip()
        return raw
