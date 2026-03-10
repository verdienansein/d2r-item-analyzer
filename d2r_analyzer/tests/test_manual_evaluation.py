from d2r_analyzer.evaluator import ManualEvaluator

test_rules = {
    "ring": [
        {
            "quality": "magic",
            "base_score": 0,
            "affixes_scores": [
                {
                    "stat": "faster_cast_rate",
                    "max_value": 10,
                    "min_value": 1,
                    "score": 50,
                },
                {
                    "stat": "all_resistances",
                    "max_value": 15,
                    "min_value": 3,
                    "score": 50,
                },
                {
                    "stat": "better_chance_of_getting_magic_items",
                    "max_value": 40,
                    "min_value": 20,
                    "score": 100,
                },
            ],
        },
        {
            "quality": "unique",
            "base_score": 100,
            "affixes_scores": [],
        },
    ],
    "amulet": [
        {
            "quality": "magic",
            "base_score": 0,
            "affixes_scores": [
                {
                    "stat": "lightning_skills",
                    "max_value": 3,
                    "min_value": 1,
                    "score": 50,
                },
                {
                    "stat": "life",
                    "max_value": 100,
                    "min_value": 20,
                    "score": 50,
                },
            ],
        }
    ],
}

evaluator = ManualEvaluator(test_rules)


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
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == "D", (
        "Expected grade 'D' for the item"
    )


def test_unique_ring() -> None:
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
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == "S", (
        "Expected grade 'S' for the item"
    )


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
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == "S", (
        "Expected grade 'S' for the item"
    )


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


def test_lightning_skills_and_life_ring() -> None:
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
    actual_verdict = evaluator.evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert evaluator.evaluate_item(item_info).get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )
