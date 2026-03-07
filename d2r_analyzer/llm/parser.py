import json
import re

from pydantic import BaseModel, field_validator


def _strip_fences(text: str) -> str:
    """Strip markdown code fences and whitespace from LLM output."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


class AffixSchema(BaseModel):
    raw_text: str
    stat: str | None = None
    value: float | int | None = None
    unit: str | None = None

    @field_validator("value", mode="before")
    @classmethod
    def normalize_value(cls, v):
        if v in (None, "", "null"):
            return None

        if isinstance(v, list) and len(v) >= 2:
            nums = [n for n in v if isinstance(n, (int, float))]
            if len(nums) >= 2:
                return (nums[0] + nums[1]) / 2

        if isinstance(v, dict):
            min_v = v.get("min")
            max_v = v.get("max")
            if isinstance(min_v, (int, float)) and isinstance(max_v, (int, float)):
                return (min_v + max_v) / 2

        if isinstance(v, str):
            # Accept many real-world patterns: "12-45", "12 to 45", "43 of 55".
            nums = re.findall(r"-?\d+(?:\.\d+)?", v)
            if len(nums) >= 2:
                a = float(nums[0])
                b = float(nums[1])
                return (a + b) / 2
            if len(nums) == 1:
                return float(nums[0])

        return v


class ItemSchema(BaseModel):
    name: str | None = None
    base_type: str | None = None
    quality: str | None = "unknown"
    item_level: int | None = None
    required_level: int | None = None
    affixes: list[AffixSchema] = []
    sockets: int = 0
    is_ethereal: bool = False
    defense: int | None = None
    damage: str | None = None

    @field_validator("quality", mode="before")
    @classmethod
    def normalize_quality(cls, v: str | None) -> str:
        if v is None:
            return "unknown"
        return v.lower().strip()

    @field_validator("sockets", mode="before")
    @classmethod
    def normalize_sockets(cls, v):
        if v in (None, "", "null"):
            return 0
        if isinstance(v, str):
            digits = "".join(ch for ch in v if ch.isdigit())
            return int(digits) if digits else 0
        return v

    @field_validator("damage", mode="before")
    @classmethod
    def normalize_damage(cls, v):
        if isinstance(v, dict):
            min_dmg = v.get("min")
            max_dmg = v.get("max")
            if min_dmg is not None and max_dmg is not None:
                return f"{min_dmg}-{max_dmg}"
            return json.dumps(v)
        return v


class EvaluationSchema(BaseModel):
    grade: str
    verdict: str
    best_build: str | None
    trade_value: str
    reasoning: str
    good_affixes: list[str]
    wasted_slots: list[str]
    roll_quality: str


def parse_item(raw: dict | str) -> ItemSchema:
    """Validate LLM output against schema. Raises ValidationError if malformed."""
    if isinstance(raw, str):
        raw = json.loads(_strip_fences(raw))
    return ItemSchema(**raw)


def parse_evaluation(raw: dict | str) -> EvaluationSchema:
    if isinstance(raw, str):
        raw = _strip_fences(raw)
        if not raw:
            raise ValueError("LLM returned empty response for evaluation")
        raw = json.loads(raw)
    return EvaluationSchema(**raw)
