from pydantic import BaseModel, field_validator


class AffixSchema(BaseModel):
    raw_text: str
    stat: str | None = None
    value: float | int | None = None
    unit: str | None = None


class ItemSchema(BaseModel):
    name: str | None = None
    base_type: str | None = None
    quality: str = "unknown"
    item_level: int | None = None
    required_level: int | None = None
    affixes: list[AffixSchema] = []
    sockets: int = 0
    is_ethereal: bool = False
    defense: int | None = None
    damage: str | None = None

    @field_validator("quality")
    @classmethod
    def normalize_quality(cls, v: str) -> str:
        return v.lower().strip()


def parse_item(raw: dict) -> ItemSchema:
    """Validate LLM output against schema. Raises ValidationError if malformed."""
    return ItemSchema(**raw)
