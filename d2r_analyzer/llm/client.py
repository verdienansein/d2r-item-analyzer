from openai import OpenAI

try:
    from d2r_analyzer.llm.prompts import ITEM_EXTRACTION_PROMPT
except ModuleNotFoundError:
    from llm.prompts import ITEM_EXTRACTION_PROMPT


class LLMClient:
    def __init__(self, model_name: str, base_url: str, api_key: str):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def extract_item_info(self, image_base64: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": ITEM_EXTRACTION_PROMPT},
                        {
                            "type": "input_image",
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
