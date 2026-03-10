class ManualEvaluator:
    def __init__(self, evaluation_rules: dict) -> None:
        self.evaluation_rules = evaluation_rules

    def evaluate_item(self, item: dict) -> dict:
        evaluation = {}
        good_affixes = []
        score = 0
        if item["quality"] == "unique":
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "S"
            evaluation["good_affixes"] = good_affixes
            return evaluation

        for rule in self.evaluation_rules.get(item["base_type"].lower(), []):
            if rule["quality"] == item["quality"]:
                for affix_rule in rule["affixes_scores"]:
                    for affix in item["affixes"]:
                        if affix["stat"] == affix_rule["stat"]:
                            if (
                                affix_rule["min_value"]
                                <= affix["value"]
                                <= affix_rule["max_value"]
                            ):
                                score += affix_rule["score"] * (
                                    affix["value"] / affix_rule["max_value"]
                                )
                                good_affixes.append(affix)

        if score >= 90:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "S"
        elif score >= 80:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "A"
        elif score >= 70:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "B"
        elif score >= 60:
            evaluation["verdict"] = "KEEP"
            evaluation["grade"] = "C"
        else:
            evaluation["verdict"] = "DISCARD"
            evaluation["grade"] = "D"

        evaluation["good_affixes"] = good_affixes
        return evaluation
