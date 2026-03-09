class ManualEvaluator:
    def __init__(self):
        pass

    def evaluate_item(self, item: dict) -> dict:
        evaluation = {}
        score = 0
        if item["quality"] == "unique":
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "S"
        if item["quality"] == "magic":
            for affix in item["affixes"]:
                if affix.get("stat") == "faster_cast_rate" and affix.get("value") >= 10:
                    score += (affix.get("value") / 20) * 50
                    evaluation["good_affixes"] = evaluation.get("good_affixes", []) + [affix.get("raw_text")]
                if affix.get("stat") == "all_resistances" and affix.get("value") >= 10:
                    score += (affix.get("value") / 30) * 50
                    evaluation["good_affixes"] = evaluation.get("good_affixes", []) + [affix.get("raw_text")]
                if (
                    affix.get("stat") == "better_chance_of_getting_magic_items"
                    and affix.get("value") >= 25
                ):
                    score += (affix.get("value") / 40) * 100
                    evaluation["good_affixes"] = evaluation.get("good_affixes", []) + [affix.get("raw_text")]
                if (
                    (affix.get("stat") == "lightning_skills" or affix.get("stat") == "fire_skills" or affix.get("stat") == "cold_skills")
                    and affix.get("value") >= 1
                ):
                    score += (affix.get("value") / 3) * 50
                    evaluation["good_affixes"] = evaluation.get("good_affixes", []) + [affix.get("raw_text")]
                if affix.get("stat") == "life" and affix.get("value") >= 90:
                    score += (affix.get("value") / 100) * 50
                    evaluation["good_affixes"] = evaluation.get("good_affixes", []) + [affix.get("raw_text")]

        if score >= 75:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "S"
        elif score >= 50:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "A"
        elif score >= 25:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "B"
        else:
            evaluation["verdict"] = "DISCARD"
            evaluation["grade"] = "C"

        return evaluation
