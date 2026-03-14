class ManualEvaluator:
    def __init__(self, evaluation_rules: dict) -> None:
        self.evaluation_rules = evaluation_rules

    def evaluate_item(self, item: dict) -> dict:
        evaluation = {}
        good_affixes = []
        score = 0

        if item["quality"] == "unique":
            unique_rules = self.evaluation_rules.get("uniques", {})
            unique_info = unique_rules.get(item["name"].lower())
            if unique_info:
                score = unique_info.get("score", 0)
                good_affixes = item.get("affixes", [])
        else:
            for rule in self.evaluation_rules.get(
                item["base_type"].lower().replace(" ", "_"), []
            ):
                if rule["quality"] == item["quality"]:
                    score += rule.get("base_score", 0)
                    for affix_rule in rule["affixes_scores"]:
                        for affix in item["affixes"]:
                            if affix["stat"] == affix_rule["stat"]:
                                if (
                                    affix_rule["min_value"]
                                    <= affix["value"]
                                    <= affix_rule["max_value"]
                                ):
                                    score += affix_rule["score"] * (
                                        (affix["value"] - affix_rule["min_value"])
                                        / (
                                            affix_rule["max_value"]
                                            - affix_rule["min_value"]
                                        )
                                    )
                                    good_affixes.append(affix)

        score = min(score, 100)

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

        evaluation["score"] = score
        evaluation["reasoning"] = f"Item evaluated with a score of {score}"
        evaluation["good_affixes"] = good_affixes
        return evaluation
