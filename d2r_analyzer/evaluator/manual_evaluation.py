

def evaluate_item(item: dict) -> dict:
    evaluation = {}
    if item["quality"] == "magic":
        for affix in item["affixes"]:
            if affix.get("stat") == "faster_cast_rate" and affix.get("value") >= 10:
                evaluation["verdict"] = "KEEP"

    return evaluation
