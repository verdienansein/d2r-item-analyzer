import json
from pathlib import Path

from d2r_analyzer.evaluator import ManualEvaluator

test_rules_file = Path(__file__).resolve().parent / "config_rules/test_rules.json"

with open(test_rules_file, "r") as f:
    manual_rules = json.load(f)
evaluator = ManualEvaluator(manual_rules)


def test_no_valuable_affixes() -> None:
    item_info = {
        "name": "Simple Ring of the Novice",
        "base_type": "Ring",
        "quality": "magic",
        "item_level": None,
        "required_level": 10,
        "affixes": [
            {
                "raw_text": "+10 to Attack Rating",
                "stat": "attack_rating",
                "value": 10,
                "unit": "",
            },
            {
                "raw_text": "+5 to Strength",
                "stat": "strength",
                "value": 5,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "DISCARD"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "D", "Expected grade 'D' for the item"


def test_unique_magefist() -> None:
    item_info = {
        "name": "Magefist",
        "base_type": "Gloves",
        "quality": "unique",
        "item_level": None,
        "required_level": 60,
        "affixes": [],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "A", "Expected grade 'A' for the item"


def test_unique_harlequin_crest() -> None:
    item_info = {
        "name": "Harlequin Crest",
        "base_type": "Shako",
        "quality": "unique",
        "item_level": None,
        "required_level": 62,
        "affixes": [],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", "Expected grade 'S' for the item"


def test_unique_stone_of_jordan() -> None:
    item_info = {
        "name": "The Stone of Jordan",
        "base_type": "Ring",
        "quality": "unique",
        "item_level": None,
        "required_level": 60,
        "affixes": [],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", "Expected grade 'S' for the item"


def test_ring_evaluation() -> None:
    item_info = {
        "name": "Scintillating Ring of the Apprentice",
        "base_type": "Ring",
        "quality": "magic",
        "item_level": None,
        "required_level": 59,
        "affixes": [
            {
                "raw_text": "+10% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 10,
                "unit": "%",
            },
            {
                "raw_text": "+15 All Resistances",
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", "Expected grade 'S' for the item"


def test_mf_ring_evaluation() -> None:
    item_info = {
        "name": "Fortuitous Ring of Fortune",
        "base_type": "Ring",
        "quality": "magic",
        "item_level": None,
        "required_level": 31,
        "affixes": [
            {
                "raw_text": "37% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 36,
                "unit": "%",
            }
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == "A", (
        "Expected grade 'A' for the item"
    )


def test_mf_ring_fire_resist_evaluation() -> None:
    item_info = {
        "name": "Fortuitous Ring of Fire Resist",
        "base_type": "Ring",
        "quality": "magic",
        "item_level": None,
        "required_level": 31,
        "affixes": [
            {
                "raw_text": "20% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+30% Fire Resist",
                "stat": "fire_resist",
                "value": 30,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "C", "Expected grade 'C' for the item"


def test_lightning_skills_and_life_amulet() -> None:
    item_info = {
        "name": "Powered Amulet of the Whale",
        "base_type": "Amulet",
        "quality": "magic",
        "item_level": None,
        "required_level": 45,
        "affixes": [
            {
                "raw_text": "+3 to Lightning Skills (Sorceress Only)",
                "stat": "lightning_skills",
                "value": 3,
                "unit": None,
            },
            {"raw_text": "+100 to Life", "stat": "life", "value": 100, "unit": None},
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_lightning_skills_and_fcr_amulet() -> None:
    item_info = {
        "name": "Powered Amulet of the Apprentice",
        "base_type": "Amulet",
        "quality": "magic",
        "item_level": None,
        "required_level": 45,
        "affixes": [
            {
                "raw_text": "+3 to Lightning Skills (Sorceress Only)",
                "stat": "lightning_skills",
                "value": 3,
                "unit": None,
            },
            {
                "raw_text": "+10% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 10,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_grand_charm() -> None:
    item_info = {
        "name": "Giant Grand Charm of Vita",
        "base_type": "Grand Charm",
        "quality": "magic",
        "item_level": None,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+1 to Lightning Skills (Sorceress Only)",
                "stat": "lightning_skills",
                "value": 1,
                "unit": None,
            },
            {
                "raw_text": "+12% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 12,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_rare_ring() -> None:
    item_info = {
        "name": "Rare Ring",
        "base_type": "Ring",
        "quality": "rare",
        "item_level": None,
        "required_level": 59,
        "affixes": [
            {"stat": "faster_cast_rate", "value": 10, "unit": "%"},
            {
                "raw_text": "+40 to Life",
                "stat": "life",
                "value": 40,
                "unit": "",
            },
            {
                "raw_text": "+50 to Fire Resist",
                "stat": "fire_resist",
                "value": 50,
                "unit": "",
            },
            {
                "raw_text": "+50 to Lightning Resist",
                "stat": "lightning_resist",
                "value": 50,
                "unit": "",
            },
            {
                "raw_text": "+50 to Cold Resist",
                "stat": "cold_resist",
                "value": 50,
                "unit": "",
            },
            {
                "raw_text": "25% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 25,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    actual_evaluation = evaluator.evaluate_item(item_info)

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", "Expected grade 'S' for the item"

    assert (
        actual_evaluation.get("score", 0) > 90
        and actual_evaluation.get("score", 0) <= 100
    ), "Expected score above 90 for the item"


def test_small_charm() -> None:
    item_info = {
        "name": "Small Charm of the Apprentice",
        "base_type": "Small Charm",
        "quality": "magic",
        "item_level": None,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "7% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 7,
                "unit": "%",
            },
            {
                "raw_text": "+15 to Mana",
                "stat": "mana",
                "value": 15,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_large_charm() -> None:
    item_info = {
        "name": "Shimmering Large Charm of Vita",
        "base_type": "Large Charm",
        "quality": "magic",
        "item_level": None,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+35 to Life",
                "stat": "life",
                "value": 35,
                "unit": "",
            },
            {
                "raw_text": "All Resistances +8",
                "stat": "all_resistances",
                "value": 8,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_magic_jewel() -> None:
    item_info = {
        "name": "Shimmering Jewel of Fervor",
        "base_type": "Jewel",
        "quality": "magic",
        "item_level": None,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+15% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 15,
                "unit": "%",
            },
            {
                "raw_text": "+15 to All Resistances",
                "stat": "all_resistances",
                "value": 7,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "A"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert (
        actual_evaluation.get("score", 0) >= 80
        and actual_evaluation.get("score", 0) <= 90
    ), (
        f"Expected score between 80 and 90 for the item, got {actual_evaluation.get('score', 0)}"
    )
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_magic_jewel_ed() -> None:
    item_info = {
        "name": "Ruby Jewel of Fervor",
        "base_type": "Jewel",
        "quality": "magic",
        "item_level": None,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+15% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 15,
                "unit": "%",
            },
            {
                "raw_text": "+40% Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 40,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert (
        actual_evaluation.get("score", 0) >= 90
        and actual_evaluation.get("score", 0) <= 100
    ), (
        f"Expected score between 90 and 100 for the item, got {actual_evaluation.get('score', 0)}"
    )
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )


def test_rare_sword() -> None:
    item_info = {
        "name": "Corpse Hew",
        "name_color": "yellow",
        "base_type": "weapon",
        "quality": "rare",
        "item_level": None,
        "required_level": 44,
        "affixes": [
            {
                "raw_text": "+20% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+142 to Attack Rating",
                "stat": "attack_rating",
                "value": 142,
                "unit": None,
            },
            {
                "raw_text": "+150% Damage to Demons",
                "stat": "damage_to_demons",
                "value": 150,
                "unit": "%",
            },
            {
                "raw_text": "+157 to Attack Rating Against Demons",
                "stat": "attack_rating_against_demons",
                "value": 157,
                "unit": None,
            },
            {
                "raw_text": "Adds 41-66 Fire Damage",
                "stat": "fire_damage",
                "value": 53.5,
                "unit": None,
            },
            {
                "raw_text": "4% Life Stolen per Hit",
                "stat": "life_stolen_per_hit",
                "value": 4,
                "unit": "%",
            },
            {
                "raw_text": "Repairs 1 Durability in 33 Seconds",
                "stat": "repair_durability",
                "value": 1,
                "unit": None,
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": {"min": 50, "max": 94},
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) > 40
        and actual_evaluation.get("score", 0) <= 60
    ), "Expected score between 40 and 60 for the item"

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "C", "Expected grade 'C' for the item"


def test_rare_weapon_discard() -> None:
    item_info = {
        "name": "Eagle Spawn Maul",
        "name_color": "brown",
        "base_type": "weapon",
        "quality": "unique",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+2 to Combat Skills (Barbarian Only)",
                "stat": "combat_skills",
                "value": 2,
                "unit": "",
            },
            {
                "raw_text": "+69% Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 69,
                "unit": "%",
            },
            {
                "raw_text": "+12 to Maximum Damage",
                "stat": "maximum_damage",
                "value": 12,
                "unit": "",
            },
            {
                "raw_text": "+127 to Attack Rating",
                "stat": "attack_rating",
                "value": 127,
                "unit": "",
            },
            {
                "raw_text": "Adds 4-14 Cold Damage",
                "stat": "cold_damage",
                "value": 9,
                "unit": "",
            },
            {"raw_text": "+10 to Life", "stat": "life", "value": 10, "unit": ""},
            {
                "raw_text": "+50% Damage to Undead",
                "stat": "damage_to_undead",
                "value": 50,
                "unit": "%",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": {"min": 50, "max": 84},
    }

    expected_verdict = "DISCARD"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 0
        and actual_evaluation.get("score", 0) < 40
    ), "Expected score below 40 for the item"

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "D", "Expected grade 'D' for the item"


def test_grade_s_rare_weapon() -> None:
    item_info = {
        "name": "Brimstone Maul",
        "name_color": "yellow",
        "base_type": "weapon",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+40% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 40,
                "unit": "%",
            },
            {
                "raw_text": "+350% Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 350,
                "unit": "%",
            },
            {
                "raw_text": "+40 to Maximum Damage",
                "stat": "maximum_damage",
                "value": 40,
                "unit": "",
            },
            {
                "raw_text": "+450 to Attack Rating",
                "stat": "attack_rating",
                "value": 450,
                "unit": "",
            },
            {
                "raw_text": "Repairs 1 Durability in 33 Seconds",
                "stat": "repairs_durability",
                "value": 33,
                "unit": "sec",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": {"min": 50, "max": 84},
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 90
        and actual_evaluation.get("score", 0) <= 100
    ), (
        f"Expected score between 90 and 100 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", (
        f"Expected grade 'S' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_grade_C_caster_rare_weapon() -> None:
    item_info = {
        "name": "Brimstone staff",
        "name_color": "yellow",
        "base_type": "weapon",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+20% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+3 to Cold Skills (Sorceress Only)",
                "stat": "cold_skills",
                "value": 3,
                "unit": "",
            },
            {
                "raw_text": "+30% Fire Resist",
                "stat": "fire_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+20 to Life",
                "stat": "life",
                "value": 20,
                "unit": "",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": {"min": 50, "max": 84},
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 40
        and actual_evaluation.get("score", 0) <= 60
    ), (
        f"Expected score between 40 and 60 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "C", (
        f"Expected grade 'C' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_rare_gloves() -> None:
    item_info = {
        "name": "Vampire Hand of the Leech",
        "name_color": "yellow",
        "base_type": "Gloves",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+20% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+2 to Javelin and Spear Skills (Amazon Only)",
                "stat": "javelin_and_spear_skills",
                "value": 2,
                "unit": "",
            },
            {
                "raw_text": "+20% Fire Resist",
                "stat": "fire_resist",
                "value": 20,
                "unit": "%",
            },
            {"stat": "better_chance_of_getting_magic_items", "value": 18, "unit": "%"},
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 80
        and actual_evaluation.get("score", 0) <= 90
    ), (
        f"Expected score between 80 and 90 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "A", (
        f"Expected grade 'A' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_rare_boots() -> None:
    item_info = {
        "name": "Gorefoot",
        "name_color": "yellow",
        "base_type": "Boots",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+30% Faster Run/Walk",
                "stat": "faster_run_walk",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+150% Enhanced Defense",
                "stat": "enhanced_defense",
                "value": 150,
                "unit": "%",
            },
            {
                "raw_text": "+20% Cold Resist",
                "stat": "cold_resist",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+20% Fire Resist",
                "stat": "fire_resist",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+70% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 70,
                "unit": "%",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 80
        and actual_evaluation.get("score", 0) <= 90
    ), (
        f"Expected score between 80 and 90 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "A", (
        f"Expected grade 'A' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_rare_helmet() -> None:
    item_info = {
        "name": "Arreat Helm",
        "name_color": "yellow",
        "base_type": "Helmet",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+1 to Sorceress Skill Levels",
                "stat": "sorceress_skills",
                "value": 1,
                "unit": "",
            },
            {
                "raw_text": "+20% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "Faster run/walk +30%",
                "stat": "faster_run_walk",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+30 to all resistances",
                "stat": "all_resistances",
                "value": 30,
                "unit": "",
            },
            {
                "raw_text": "better chance of getting magic items +35",
                "stat": "better_chance_of_getting_magic_items",
                "value": 35,
                "unit": "%",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 80
        and actual_evaluation.get("score", 0) < 90
    ), (
        f"Expected score between 80 and 90 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "A", (
        f"Expected grade 'A' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_rare_armor() -> None:
    item_info = {
        "name": "Pale Armor",
        "name_color": "yellow",
        "base_type": "Armor",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+200% Enhanced Defense",
                "stat": "enhanced_defense",
                "value": 200,
                "unit": "%",
            },
            {
                "raw_text": "+30% Cold Resist",
                "stat": "cold_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+30% Fire Resist",
                "stat": "fire_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+24% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 24,
                "unit": "%",
            },
            {
                "stat": "life",
                "value": 40,
                "unit": "",
            },
            {
                "stat": "strength",
                "value": 20,
                "unit": "",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 70
        and actual_evaluation.get("score", 0) < 80
    ), (
        f"Expected score between 70 and 80 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "B", (
        f"Expected grade 'B' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_rare_belt() -> None:
    item_info = {
        "name": "String of Ears",
        "name_color": "yellow",
        "base_type": "Belt",
        "quality": "rare",
        "item_level": 85,
        "required_level": 39,
        "affixes": [
            {
                "raw_text": "+30% Light Resist",
                "stat": "light_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+30% Cold Resist",
                "stat": "cold_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+30% Fire Resist",
                "stat": "fire_resist",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+24% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 24,
                "unit": "%",
            },
            {
                "stat": "life",
                "value": 140,
                "unit": "",
            },
        ],
        "sockets": None,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 90
        and actual_evaluation.get("score", 0) <= 100
    ), (
        f"Expected score between 90 and 100 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", (
        f"Expected grade 'S' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_set_item() -> None:
    item_info = {
        "name": "Tal Rasha's Horadric Crest",
        "base_type": "Mail",
        "quality": "set",
        "item_level": None,
        "required_level": 45,
        "affixes": [],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")
    assert (
        actual_evaluation.get("score", 0) >= 80
        and actual_evaluation.get("score", 0) < 90
    ), (
        f"Expected score between 80 and 90 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "A", (
        f"Expected grade 'A' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_very_rare_amulet() -> None:
    item_info = {
        "name": "Dire Hood Amulet",
        "base_type": "Amulet",
        "quality": "rare",
        "item_level": None,
        "required_level": None,
        "affixes": [
            {
                "raw_text": "15% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 15,
                "unit": "%",
            },
            {
                "raw_text": "+1 To Necromancer Skill Levels",
                "stat": "necromancer_skills",
                "value": 1,
                "unit": "",
            },
            {
                "raw_text": "All Resistances +20",
                "stat": "all_resistances",
                "value": 20,
                "unit": "",
            },
            {
                "raw_text": "10% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 10,
                "unit": "%",
            },
            {
                "raw_text": "35% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 35,
                "unit": "%",
            },
            {
                "raw_text": "+100 To Life",
                "stat": "life",
                "value": 100,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
    }

    expected_verdict = "KEEP"
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_verdict = actual_evaluation.get("verdict", "")

    assert (
        actual_evaluation.get("score", 0) >= 90
        and actual_evaluation.get("score", 0) <= 100
    ), (
        f"Expected score between 90 and 100 for the item, got {actual_evaluation.get('score', 0)}"
    )

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert actual_evaluation.get("grade", "") == "S", (
        f"Expected grade 'S' for the item, got '{actual_evaluation.get('grade', '')}'"
    )


def test_unknown_unique_discarded() -> None:
    item_info = {
        "name": "Doom Shard",
        "base_type": "ring",
        "quality": "unique",
        "item_level": 40,
        "required_level": 20,
        "affixes": [],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_magic_amulet_life_below_min_discarded() -> None:
    item_info = {
        "name": "Coral Amulet of the Jackal",
        "base_type": "amulet",
        "quality": "magic",
        "item_level": 30,
        "required_level": 10,
        "affixes": [
            {"raw_text": "+10 to Life", "stat": "life", "value": 10, "unit": ""},
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_magic_ring_max_mf() -> None:
    item_info = {
        "name": "Fortuitous Ring of Fortune",
        "base_type": "ring",
        "quality": "magic",
        "item_level": 85,
        "required_level": 55,
        "affixes": [
            {
                "raw_text": "40% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 40,
                "unit": "%",
            }
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) == 100
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "S"


def test_magic_ring_min_mf_discarded() -> None:
    item_info = {
        "name": "Plodding Ring of Fortune",
        "base_type": "ring",
        "quality": "magic",
        "item_level": 30,
        "required_level": 10,
        "affixes": [
            {
                "raw_text": "10% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 10,
                "unit": "%",
            }
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_rare_shield_paladin_focused() -> None:
    item_info = {
        "name": "Hallowed Aegis",
        "base_type": "shield",
        "quality": "rare",
        "item_level": 85,
        "required_level": 62,
        "affixes": [
            {
                "raw_text": "+2 to Paladin Skills",
                "stat": "paladin_skills",
                "value": 2,
                "unit": "",
            },
            {
                "raw_text": "25 All Resistances",
                "stat": "all_resistances",
                "value": 25,
                "unit": "",
            },
            {
                "raw_text": "25% Faster Block Rate",
                "stat": "faster_block_rate",
                "value": 25,
                "unit": "%",
            },
            {
                "raw_text": "20% Increased Chance of Blocking",
                "stat": "increased_chance_of_blocking",
                "value": 20,
                "unit": "%",
            },
            {"raw_text": "+50 to Life", "stat": "life", "value": 50, "unit": ""},
            {
                "raw_text": "+30% Fire Resist",
                "stat": "fire_resist",
                "value": 30,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": 200,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 80 <= actual_score < 90, f"Expected score 80–90, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "A"


def test_rare_shield_resists_only_discarded() -> None:
    item_info = {
        "name": "Ember Rampart",
        "base_type": "shield",
        "quality": "rare",
        "item_level": 85,
        "required_level": 40,
        "affixes": [
            {
                "raw_text": "+35% Fire Resist",
                "stat": "fire_resist",
                "value": 35,
                "unit": "%",
            },
            {
                "raw_text": "+35% Lightning Resist",
                "stat": "lightning_resist",
                "value": 35,
                "unit": "%",
            },
            {
                "raw_text": "+10% Cold Resist",
                "stat": "cold_resist",
                "value": 10,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": 120,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) < 40
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_grand_charm_life_only() -> None:
    item_info = {
        "name": "Mammoth Grand Charm of Vita",
        "base_type": "grand charm",
        "quality": "magic",
        "item_level": 85,
        "required_level": 50,
        "affixes": [
            {"raw_text": "+40 to Life", "stat": "life", "value": 40, "unit": ""},
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) == 50
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "C"


def test_grand_charm_attack_rating_below_min_discarded() -> None:
    item_info = {
        "name": "Grand Charm of Dexterity",
        "base_type": "grand charm",
        "quality": "magic",
        "item_level": 50,
        "required_level": 25,
        "affixes": [
            {
                "raw_text": "+15 to Attack Rating",
                "stat": "attack_rating",
                "value": 15,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_belt_useless_stat_discarded() -> None:
    item_info = {
        "name": "Mana Cord",
        "base_type": "belt",
        "quality": "rare",
        "item_level": 60,
        "required_level": 30,
        "affixes": [
            {"raw_text": "+100 to Mana", "stat": "mana", "value": 100, "unit": ""},
            {"raw_text": "+80 to Mana", "stat": "mana", "value": 80, "unit": ""},
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_armor_resists_only_discarded() -> None:
    item_info = {
        "name": "Shadow Robe",
        "base_type": "armor",
        "quality": "rare",
        "item_level": 85,
        "required_level": 50,
        "affixes": [
            {
                "raw_text": "+25% Cold Resist",
                "stat": "cold_resist",
                "value": 25,
                "unit": "%",
            },
            {
                "raw_text": "+20% Fire Resist",
                "stat": "fire_resist",
                "value": 20,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": 300,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) < 40
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_large_charm_single_weak_resist_discarded() -> None:
    item_info = {
        "name": "Large Charm of Flame",
        "base_type": "large charm",
        "quality": "magic",
        "item_level": 40,
        "required_level": 20,
        "affixes": [
            {
                "raw_text": "+8% Fire Resist",
                "stat": "fire_resist",
                "value": 8,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) < 40
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_jewel_only_life_discarded() -> None:
    item_info = {
        "name": "Jewel of the Leech",
        "base_type": "jewel",
        "quality": "magic",
        "item_level": 60,
        "required_level": 30,
        "affixes": [
            {"raw_text": "+20 to Life", "stat": "life", "value": 20, "unit": ""},
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) < 40
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_jewel_score_capped_at_100() -> None:
    item_info = {
        "name": "Ruby Jewel of Fervor",
        "base_type": "jewel",
        "quality": "magic",
        "item_level": 85,
        "required_level": 49,
        "affixes": [
            {
                "raw_text": "+15% Increased Attack Speed",
                "stat": "increased_attack_speed",
                "value": 15,
                "unit": "%",
            },
            {
                "raw_text": "+15 All Resistances",
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
            {
                "raw_text": "+40% Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 40,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) == 100, "Score must be capped at 100"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "S"


def test_gloves_no_useful_stats_discarded() -> None:
    item_info = {
        "name": "Bramble Mitts",
        "base_type": "gloves",
        "quality": "rare",
        "item_level": 50,
        "required_level": 20,
        "affixes": [
            {
                "raw_text": "+5% Fire Resist",
                "stat": "fire_resist",
                "value": 5,
                "unit": "%",
            },
            {
                "raw_text": "+5% Cold Resist",
                "stat": "cold_resist",
                "value": 5,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_boots_low_frw_only_discarded() -> None:
    item_info = {
        "name": "Slow Greaves",
        "base_type": "boots",
        "quality": "rare",
        "item_level": 60,
        "required_level": 25,
        "affixes": [
            {
                "raw_text": "10% Faster Run/Walk",
                "stat": "faster_run_walk",
                "value": 10,
                "unit": "%",
            },
            {
                "raw_text": "+5% Fire Resist",
                "stat": "fire_resist",
                "value": 5,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) < 40
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_grand_charm_rare() -> None:
    item_info = {
        "name": "Grand Charm of the Bear",
        "base_type": "grand charm",
        "quality": "rare",
        "item_level": 85,
        "required_level": 50,
        "affixes": [
            {
                "stat": "life",
                "value": 40,
                "unit": "%",
            },
            {
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
            {
                "stat": "better_chance_of_getting_magic_items",
                "value": 12,
                "unit": "",
            },
            {
                "stat": "mana",
                "value": 59,
                "unit": "",
            },
            {
                "stat": "faster_hit_recovery",
                "value": 12,
                "unit": "",
            },
            {
                "stat": "faster_run_walk",
                "value": 3,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", 0) == 100, "Score must be capped at 100"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "S"


def test_rare_weapon_no_useful_stats_discarded() -> None:
    item_info = {
        "name": "Fiend Barb",
        "base_type": "Bardiche",
        "quality": "rare",
        "item_level": None,
        "required_level": 16,
        "affixes": [
            {
                "raw_text": "+1 to Combat Skills (Barbarian Only)",
                "stat": "combat_skills",
                "value": 1,
                "unit": "",
            },
            {
                "raw_text": "+63% Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 63,
                "unit": "%",
            },
            {
                "raw_text": "+1 to Maximum Damage",
                "stat": "maximum_damage",
                "value": 1,
                "unit": "",
            },
            {
                "raw_text": "+46 to Attack Rating",
                "stat": "attack_rating",
                "value": 46,
                "unit": "",
            },
            {
                "raw_text": "7% Mana stolen per hit",
                "stat": "mana_stolen_per_hit",
                "value": 7,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
    }
    actual_evaluation = evaluator.evaluate_item(item_info)
    assert actual_evaluation.get("score", -1) == 0
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"


def test_rare_jewel_A_stats() -> None:
    item_info = {
        "name": "Smasher Flange Jewel",
        "base_type": "Jewel",
        "quality": "rare",
        "item_level": None,
        "required_level": None,
        "affixes": [
            {
                "raw_text": "All Resistances +15",
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
            {
                "raw_text": "7% Better Chance of Getting Magic Items",
                "stat": "better_chance_of_getting_magic_items",
                "value": 7,
                "unit": "%",
            },
            {
                "raw_text": "+20 To Mana",
                "stat": "mana",
                "value": 20,
                "unit": "",
            },
            {
                "raw_text": "7% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 7,
                "unit": "%",
            },
            {
                "raw_text": "+20 To Life",
                "stat": "life",
                "value": 20,
                "unit": "",
            },
            {
                "raw_text": "+9 To Strength",
                "stat": "strength",
                "value": 9,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 80 <= actual_score < 90, f"Expected score 80–90, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "A"


def test_rare_jewel_S_stats() -> None:
    item_info = {
        "name": "Crazy Flange Jewel",
        "base_type": "Jewel",
        "quality": "rare",
        "item_level": None,
        "required_level": None,
        "affixes": [
            {
                "raw_text": "All Resistances +15",
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
            {
                "raw_text": "Increased Attack Speed +15%",
                "stat": "increased_attack_speed",
                "value": 15,
                "unit": "%",
            },
            {
                "raw_text": "+40% To Enhanced Damage",
                "stat": "enhanced_damage",
                "value": 40,
                "unit": "%",
            },
            {
                "raw_text": "7% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 7,
                "unit": "%",
            },
            {
                "raw_text": "+20 To Life",
                "stat": "life",
                "value": 20,
                "unit": "",
            },
            {
                "raw_text": "+9 To Maximum Damage",
                "stat": "maximum_damage",
                "value": 9,
                "unit": "",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 90 <= actual_score <= 100, f"Expected score 90-100, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "S"


def test_rare_greaves() -> None:
    item_info = {
        "name": "Greaves",
        "base_type": "boots",
        "quality": "rare",
        "item_level": None,
        "required_level": 38,
        "affixes": [
            {
                "raw_text": "+30% Faster Run/Walk",
                "stat": "faster_run_walk",
                "value": 30,
                "unit": "%",
            },
            {
                "raw_text": "+10% Faster Hit Recovery",
                "stat": "faster_hit_recovery",
                "value": 10,
                "unit": "%",
            },
            {
                "raw_text": "+46% Enhanced Defense",
                "stat": "enhanced_defense",
                "value": 46,
                "unit": "%",
            },
            {
                "raw_text": "+9 To Dexterity",
                "stat": "dexterity",
                "value": 9,
                "unit": "",
            },
            {
                "raw_text": "Lightning Resist +38%",
                "stat": "lightning_resist",
                "value": 38,
                "unit": "%",
            },
            {
                "raw_text": "Poison Resist +39%",
                "stat": "poison_resist",
                "value": 39,
                "unit": "%",
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 70 <= actual_score < 80, f"Expected score 70–80, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "B"


def test_rare_circlet_grade_A() -> None:
    item_info = {
        "name": "Circlet",
        "base_type": "helmet",
        "quality": "rare",
        "item_level": None,
        "required_level": 38,
        "affixes": [
            {
                "raw_text": "+2 To Warlock Skills",
                "stat": "warlock_skills",
                "value": 2,
                "unit": "",
            },
            {
                "raw_text": "+20% Faster Cast Rate",
                "stat": "faster_cast_rate",
                "value": 20,
                "unit": "%",
            },
            {
                "raw_text": "+91% Enhanced Defense",
                "stat": "enhanced_defense",
                "value": 91,
                "unit": "%",
            },
            {
                "raw_text": "+19 To Strength",
                "stat": "strength",
                "value": 19,
                "unit": "",
            },
            {
                "raw_text": "+15 All Resistances",
                "stat": "all_resistances",
                "value": 15,
                "unit": "",
            },
        ],
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 80 <= actual_score < 90, f"Expected score 80–90, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "A"


def test_ring_good_affixes_and_score() -> None:
    item_info = {
        "name": "Beast Touch",
        "name_color": "yellow",
        "base_type": "ring",
        "quality": "rare",
        "item_level": None,
        "required_level": 41,
        "affixes": [
            {
                "raw_text": "Replenish Life +8",
                "stat": "replenish_life",
                "value": 8,
                "unit": None,
            },
            {"raw_text": "+66 to Mana", "stat": "mana", "value": 66, "unit": None},
            {
                "raw_text": "All Resistances +3",
                "stat": "all_resistances",
                "value": 3,
                "unit": None,
            },
            {
                "raw_text": "Level 4 Poison Dagger (6/30 Charges)",
                "stat": None,
                "value": None,
                "unit": None,
            },
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    actual_good_affixes = actual_evaluation.get("good_affixes", [])
    expected_good_affixes = ["mana", "all_resistances"]
    assert actual_score < 40, f"Expected score < 40, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "DISCARD"
    assert actual_evaluation.get("grade", "") == "D"
    actual_good_affix_stats = [
        a.get("stat") if isinstance(a, dict) else a for a in actual_good_affixes
    ]
    assert set(actual_good_affix_stats) == set(expected_good_affixes), (
        f"Expected good affixes {expected_good_affixes}, got {actual_good_affix_stats}"
    )

def test_rare_ring_grade_B() -> None:
    item_info = {
    "name": "Raven Whorl",
    "name_color": "yellow",
    "base_type": "ring",
    "quality": "rare",
    "item_level": 85,
    "required_level": 66,
    "affixes": [
        {
        "raw_text": "+10% Faster Cast Rate",
        "stat": "faster_cast_rate",
        "value": 10,
        "unit": "%"
        },
        {
        "raw_text": "+5% Bonus to Attack Rating",
        "stat": "attack_rating",
        "value": 5,
        "unit": "%"
        },
        {
        "raw_text": "+26 to Attack Rating",
        "stat": "attack_rating",
        "value": 26,
        "unit": ""
        },
        {
        "raw_text": "+16 to Strength",
        "stat": "strength",
        "value": 16,
        "unit": ""
        },
        {
        "raw_text": "Cold Resist +24%",
        "stat": "cold_resist",
        "value": 24,
        "unit": "%"
        },
        {
        "raw_text": "Lightning Resist +6%",
        "stat": "lightning_resist",
        "value": 6,
        "unit": "%"
        },
        {
        "raw_text": "+5 to Light Radius",
        "stat": None,
        "value": 5,
        "unit": ""
        }
    ],
    "sockets": 0,
    "is_ethereal": False,
    "defense": None,
    "damage": None
    }

    actual_evaluation = evaluator.evaluate_item(item_info)
    actual_score = actual_evaluation.get("score", 0)
    assert 50 <= actual_score < 70, f"Expected score between 50 and 70, got {actual_score}"
    assert actual_evaluation.get("verdict", "") == "KEEP"
    assert actual_evaluation.get("grade", "") == "C"
    