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