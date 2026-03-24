import json
import re

from pydantic import BaseModel, ValidationInfo, field_validator

known_stats: set[str] = {
    "all_resistances",
    "fire_resist",
    "cold_resist",
    "lightning_resist",
    "poison_resist",
    "life",
    "mana",
    "strength",
    "lightning_skills",
    "fire_skills",
    "cold_skills",
    "martial_arts",
    "warcries",
    "traps",
    "elemental_skills",
    "summoning_skills",
    "combat_skills",
    "warlock_skills",
    "sorceress_skills",
    "necromancer_skills",
    "druid_skills",
    "paladin_skills",
    "barbarian_skills",
    "amazon_skills",
    "assassin_skills",
    "javelin_and_spear_skills",
    "faster_hit_recovery",
    "attack_rating",
    "better_chance_of_getting_magic_items",
    "faster_cast_rate",
    "increased_attack_speed",
    "faster_run_walk",
    "fire_damage",
    "enhanced_defense",
    "defense",
    "regenerate_mana",
    "all_skills",
    "all_attributes",
    "physical_damage_received_reduction",
    "increase_maximum_mana",
    "lightning_damage",
    "poison_damage",
    "poison_nova",
    "blood_golem",
    "damage_reduced",
    "maximum_damage",
    "damage_to_undead",
    "damage_to_demons",
    "enhanced_damage",
    "cold_damage",
    "life_stolen_per_hit",
    "mana_stolen_per_hit",
    "repair_durability",
    "attack_rating_against_demons",
    "faster_block_rate",
    "increased_chance_of_blocking",
    "replenish_life",
    "bone_spirit",
    "blizzard",
    "glacial_spike",
}

known_base_types: set[str] = {
    "grand charm",
    "small charm",
    "large charm",
    "jewel",
    "amulet",
    "ring",
    "helmet",
    "armor",
    "shield",
    "weapon",
    "gloves",
    "boots",
    "belt",
}


def _strip_fences(text: str) -> str:
    """Strip markdown code fences and whitespace from LLM output."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_first_json_object(text: str) -> str:
    """Extract the first top-level JSON object from arbitrary model text."""
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in model response")

    depth = 0
    in_string = False
    escape = False

    for idx in range(start, len(text)):
        ch = text[idx]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]

    raise ValueError("Unterminated JSON object in model response")


def _loads_llm_json(raw_text: str, context: str) -> dict:
    cleaned = _strip_fences(raw_text)
    if not cleaned:
        raise ValueError(f"LLM returned empty response for {context}")

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        candidate = _extract_first_json_object(cleaned)
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            preview = cleaned[:180].replace("\n", "\\n")
            raise ValueError(
                f"Invalid JSON from LLM for {context}. Response starts with: {preview}"
            ) from exc


class AffixSchema(BaseModel):
    raw_text: str
    stat: str | None = None
    value: float | int | None = None
    unit: str | None = None

    @field_validator("stat", mode="before")
    @classmethod
    def validate_stat(cls, v: str | None, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        known: set[str] | None = (info.context or {}).get("known_stats")
        if known is not None and v not in known:
            return None
        return v

    @field_validator("value", mode="before")
    @classmethod
    def normalize_value(cls, v: str | dict | list | None) -> float | int | None:
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
    name_color: str | None = None
    base_type: str | None = None
    quality: str | None = "unknown"
    item_level: int | None = None
    required_level: int | None = None
    affixes: list[AffixSchema] = []
    sockets: int = 0
    is_ethereal: bool = False
    defense: int | None = None
    damage: str | None = None

    @field_validator("item_level", "required_level", "defense", mode="before")
    @classmethod
    def convert_float_to_int(cls, v: int | float | None) -> int | None:
        if v is None:
            return None
        if isinstance(v, float):
            return int(round(v))
        return v

    @field_validator("base_type", mode="before")
    @classmethod
    def validate_base_type(cls, v: str | None, info: ValidationInfo) -> str | None:
        if v is None:
            return None
        normalized = v.lower().strip()
        known: set[str] | None = (info.context or {}).get("known_base_types")
        if known is None or normalized in known:
            return normalized

        _WEAPON_KEYWORDS = {
            "arbalest",
            "axe",
            "ballista",
            "bardiche",
            "bec-de-corbin",
            "blade",
            "bow",
            "brandistock",
            "burnt text",
            "cestus",
            "cho-ko-nu",
            "chu-ko-nu",
            "cinquedeas",
            "claw",
            "claymore",
            "cleaver",
            "club",
            "codex",
            "compendium",
            "crossbow",
            "crowbill",
            "cudgel",
            "dagger",
            "dark tome",
            "dart",
            "dirk",
            "falchion",
            "fascia",
            "fist",
            "flail",
            "flamberge",
            "gladius",
            "glaive",
            "globe",
            "grimoire",
            "halberd",
            "hammer",
            "harpoon",
            "javelin",
            "katar",
            "knife",
            "knout",
            "kris",
            "lance",
            "mace",
            "mancatcher",
            "maul",
            "naga",
            "nodachi",
            "occult tome",
            "old book",
            "orb",
            "partizan",
            "pick",
            "pike",
            "pilum",
            "poignard",
            "polearm",
            "poleaxe",
            "quhab",
            "ranseur",
            "rondel",
            "sabre",
            "scepter",
            "scimitar",
            "scourge",
            "scythe",
            "shamshir",
            "spear",
            "spetum",
            "staff",
            "stiletto",
            "suwayyah",
            "swirl",
            "sword",
            "tabar",
            "talon",
            "thresher",
            "tomahawk",
            "trident",
            "truncheon",
            "tulwar",
            "voulge",
            "wand",
            "weapon",
            "yari",
            "zweihander",
        }
        _SHIELD_KEYWORDS = {
            "shield",
            "buckler",
            "aegis",
            "ward",
            "targe",
            "kite",
            "auric",
            "tower",
            "head",
        }
        _HELMET_KEYWORDS = {
            "helm",
            "helmet",
            "skull cap",
            "crown",
            "diadem",
            "shako",
            "armet",
            "casque",
            "coif",
            "mask",
            "hat",
            "tiara",
            "circlet",
            "cap",
        }
        _ARMOR_KEYWORDS = {
            "armor",
            "plate",
            "mail",
            "coat",
            "robe",
            "cloak",
            "mantle",
            "cuirass",
            "lorica",
            "tunic",
            "hauberk",
            "breastplate",
        }
        _GLOVES_KEYWORDS = {"gloves", "gauntlets", "vambraces", "bracers", "mitts"}
        _BOOTS_KEYWORDS = {"boots", "greaves", "sandals", "shoes", "slippers", "treads"}
        _BELT_KEYWORDS = {"belt", "sash", "girdle", "cord"}
        _CHARM_KEYWORDS = {"grand charm", "large charm", "small charm", "charm"}

        for keyword in _CHARM_KEYWORDS:
            if keyword in normalized:
                if "grand" in normalized:
                    return "grand charm"
                if "large" in normalized:
                    return "large charm"
                return "small charm"
        for keyword in _WEAPON_KEYWORDS:
            if keyword in normalized:
                return "weapon"
        for keyword in _SHIELD_KEYWORDS:
            if keyword in normalized:
                return "shield"
        for keyword in _HELMET_KEYWORDS:
            if keyword in normalized:
                return "helmet"
        for keyword in _ARMOR_KEYWORDS:
            if keyword in normalized:
                return "armor"
        for keyword in _GLOVES_KEYWORDS:
            if keyword in normalized:
                return "gloves"
        for keyword in _BOOTS_KEYWORDS:
            if keyword in normalized:
                return "boots"
        for keyword in _BELT_KEYWORDS:
            if keyword in normalized:
                return "belt"
        return None

    @field_validator("quality", mode="before")
    @classmethod
    def normalize_quality(cls, v: str | None) -> str:
        if v is None:
            return "unknown"
        return v.lower().strip()

    @field_validator("sockets", mode="before")
    @classmethod
    def normalize_sockets(cls, v: str | int | None) -> int:
        if v in (None, "", "null"):
            return 0
        if isinstance(v, str):
            digits = "".join(ch for ch in v if ch.isdigit())
            return int(digits) if digits else 0
        return v

    @field_validator("defense", mode="before")
    @classmethod
    def normalize_defense(cls, v: str | int | dict | None) -> int | None:
        if v in (None, "", "null"):
            return None
        if isinstance(v, dict):
            min_v, max_v = v.get("min"), v.get("max")
            if isinstance(min_v, (int, float)) and isinstance(max_v, (int, float)):
                return (int(min_v) + int(max_v)) // 2
            return None
        if isinstance(v, str):
            nums = re.findall(r"\d+", v)
            if len(nums) >= 2:
                return (int(nums[0]) + int(nums[1])) // 2
            if len(nums) == 1:
                return int(nums[0])
            return None
        return v

    @field_validator("damage", mode="before")
    @classmethod
    def normalize_damage(cls, v: str | dict | None) -> str | None:
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
    reasoning: str
    good_affixes: list[str]
    wasted_slots: list[str]
    roll_quality: str


def parse_item(raw: dict | str) -> ItemSchema:
    if isinstance(raw, str):
        raw = _loads_llm_json(raw, context="item extraction")
    context = {"known_stats": known_stats, "known_base_types": known_base_types}
    return ItemSchema.model_validate(raw, context=context)


def parse_evaluation(raw: dict | str) -> EvaluationSchema:
    if isinstance(raw, str):
        raw = _loads_llm_json(raw, context="evaluation")
    return EvaluationSchema(**raw)
