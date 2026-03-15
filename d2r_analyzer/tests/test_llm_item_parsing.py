import base64
from pathlib import Path
from typing import NamedTuple

import pytest

from d2r_analyzer.config import config
from d2r_analyzer.evaluator import Evaluator
from d2r_analyzer.llm.parser import ItemSchema

PICTURES_DIR = Path(__file__).resolve().parent / "test_pictures"

evaluator = Evaluator(
    llm_model=config.llm_model_name,
    llm_base_url=config.llm_base_url,
    llm_api_key=config.openai_api_key,
    evaluation_mode="manual",
    manual_rules_file=str(
        Path(__file__).resolve().parent / "config_rules" / "test_rules.json"
    ),
)


class ExpectedItem(NamedTuple):
    base_type: str
    quality: str
    affix_stats: list[str]
    name: str | None = None


EXPECTED_ITEMS: dict[str, ExpectedItem] = {
    "grand_charm_1.png": ExpectedItem(
        base_type="grand charm",
        quality="magic",
        affix_stats=["lightning_skills", "life"],
    ),
    "grand_charm_2.png": ExpectedItem(
        base_type="grand charm",
        quality="magic",
        affix_stats=["javelin_and_spear_skills", "life"],
    ),
    "small_charm_1.png": ExpectedItem(
        base_type="small charm",
        quality="magic",
        affix_stats=["all_resistances", "better_chance_of_getting_magic_items"],
    ),
    "small_charm_2.png": ExpectedItem(
        base_type="small charm",
        quality="magic",
        affix_stats=["fire_resist", "better_chance_of_getting_magic_items"],
    ),
    "unique_1.png": ExpectedItem(
        base_type="gloves",
        quality="unique",
        affix_stats=[
            "fire_skills",
            "faster_cast_rate",
            "fire_damage",
            "enhanced_defense",
            "defense",
            "regenerate_mana",
        ],
    ),
    "unique_2.png": ExpectedItem(
        name="Harlequin Crest",
        base_type="helmet",
        quality="unique",
        affix_stats=[
            "all_skills",
            "all_attributes",
            "life",
            "mana",
            "physical_damage_received_reduction",
            "better_chance_of_getting_magic_items",
        ],
    ),
    "unique_3.png": ExpectedItem(
        name="The Stone of Jordan",
        base_type="ring",
        quality="unique",
        affix_stats=["all_skills", "lightning_damage", "mana", "increase_maximum_mana"],
    ),
    "rare_1.png": ExpectedItem(
        base_type="shield",
        quality="rare",
        affix_stats=[
            "poison_damage",
            "poison_nova",
            "blood_golem",
            "enhanced_defense",
            "cold_resist",
            "fire_resist",
            "lightning_resist",
            "poison_resist",
            "damage_reduced",
        ],
    ),
    "rare_2.png": ExpectedItem(
        base_type="weapon",
        quality="rare",
        affix_stats=[
            "combat_skills",
            "enhanced_damage",
            "maximum_damage",
            "attack_rating",
            "cold_damage",
            "life",
            "damage_to_undead",
        ],
    ),
    "rare_3.png": ExpectedItem(
        base_type="gloves",
        quality="rare",
        affix_stats=[
            "martial_arts",
            "life_stolen_per_hit",
            "enhanced_defense",
            "fire_resist",
        ],
    ),
    "rare_4.png": ExpectedItem(
        base_type="weapon",
        quality="rare",
        affix_stats=[
            "increased_attack_speed",
            "attack_rating",
            "damage_to_demons",
            "attack_rating_against_demons",
            "fire_damage",
            "life_stolen_per_hit",
            "repair_durability",
        ],
    ),
}

_all_images = sorted(PICTURES_DIR.glob("*.png"))


def _image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


@pytest.mark.parametrize("image_path", _all_images, ids=[p.name for p in _all_images])
def test_parse_item_from_image(image_path: Path) -> None:
    filename = image_path.name
    expected = EXPECTED_ITEMS.get(filename)
    if expected is None:
        pytest.skip(
            f"No expected item defined for '{filename}' – add it to EXPECTED_ITEMS"
        )

    image_b64 = _image_to_base64(image_path)
    item: ItemSchema = evaluator.parse_item(image_b64)

    assert isinstance(item, ItemSchema)

    if expected.name is not None:
        assert item.name is not None, "name must not be None"
        assert item.name.lower().strip() == expected.name.lower().strip(), (
            f"[{filename}] name: expected '{expected.name}', got '{item.name}'"
        )

    assert item.base_type is not None, "base_type must not be None"
    assert item.base_type.lower() == expected.base_type.lower(), (
        f"[{filename}] base_type: expected '{expected.base_type}', got '{item.base_type}'"
    )

    assert item.quality is not None, "quality must not be None"
    assert item.quality.lower() == expected.quality.lower(), (
        f"[{filename}] quality: expected '{expected.quality}', got '{item.quality}'"
    )

    assert isinstance(item.affixes, list), "affixes must be a list"
    for affix in item.affixes:
        assert affix.raw_text, (
            f"[{filename}] every affix must have a non-empty raw_text"
        )

    actual_stats = {affix.stat for affix in item.affixes if affix.stat}
    for stat in expected.affix_stats:
        assert stat in actual_stats, (
            f"[{filename}] missing expected affix stat '{stat}'. "
            f"Parsed stats: {sorted(actual_stats)}"
        )
