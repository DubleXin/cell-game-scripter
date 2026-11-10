import os

from app.src.models.rule import Rule, RuleType


def write_rules(
    data_path: str,
    neighborhood_size: int,
    rules: list[Rule],
) -> None:
    os.makedirs(
        data_path,
        exist_ok=True,
    )

    with open(
        os.path.join(data_path, ".rules"),
        "w",
    ) as f:
        f.write(f"{neighborhood_size}\n")

        f.write(f"{len(rules)}\n")

        for rule in rules:
            if rule.rule_type == RuleType.POPULATION:
                value = rule.args[0]

                f.write(
                    f"{int(rule.target_state)}_"
                    f"{int(rule.rule_type)}_"
                    f"{int(rule.comparison)}_"
                    f"{value}_"
                    f"{int(rule.result)}\n"
                )

            elif rule.rule_type == RuleType.NEIGHBOR:
                position = rule.args[0]
                value = rule.args[1]

                x, y = position

                f.write(
                    f"{int(rule.target_state)}_"
                    f"{int(rule.rule_type)}_"
                    f"{x}_{y}_"
                    f"{int(rule.comparison)}_"
                    f"{int(value)}_"
                    f"{int(rule.result)}\n"
                )
