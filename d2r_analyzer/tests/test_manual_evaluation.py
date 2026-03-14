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
    assert actual_evaluation.get("grade", "") == "B", "Expected grade 'B' for the item"


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

    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == "S", (
        "Expected grade 'S' for the item"
    )

    assert (
        evaluator.evaluate_item(item_info).get("score", 0) > 90
        and evaluator.evaluate_item(item_info).get("score", 0) <= 100
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
