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
