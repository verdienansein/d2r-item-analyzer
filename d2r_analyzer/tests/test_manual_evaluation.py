from d2r_analyzer.evaluator import ManualEvaluator


def test_ring_evaluation():
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
    actual_verdict = ManualEvaluator().evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert ManualEvaluator().evaluate_item(item_info).get("grade", "") == "A", (
        "Expected grade 'A' for the item"
    )


def test_mf_ring_evaluation():
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
                "value": 37,
                "unit": "%",
            }
        ],
        "sockets": 0,
        "is_ethereal": False,
        "defense": None,
        "damage": None,
    }
    expected_verdict = "KEEP"
    actual_verdict = ManualEvaluator().evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )
    assert ManualEvaluator().evaluate_item(item_info).get("grade", "") == "S", (
        "Expected grade 'S' for the item"
    )

def test_lightning_skills_and_life_ring():
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
        "unit": None
        },
        {
        "raw_text": "+100 to Life",
        "stat": "life",
        "value": 100,
        "unit": None
        }
    ],
    "sockets": 0,
    "is_ethereal": False,
    "defense": None,
    "damage": None
    }
    expected_verdict = "KEEP"
    expected_grade = "S"
    actual_verdict = ManualEvaluator().evaluate_item(item_info).get("verdict", "")
    assert actual_verdict == expected_verdict, (
        f"Expected verdict '{expected_verdict}', got '{actual_verdict}'"
    )  
    assert ManualEvaluator().evaluate_item(item_info).get("grade", "") == expected_grade, (
        f"Expected grade '{expected_grade}' for the item"
    )