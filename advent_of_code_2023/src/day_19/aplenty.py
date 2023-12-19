from dataclasses import dataclass


class Part:
    ratings: dict[str, int]

    def __init__(self,
                 part_string: str):
        self.ratings = {}
        for rating in part_string[1:-1].split(","):
            key, value = rating.split("=")
            self.ratings[key] = int(value)

    def get_ratings_sum(self) -> int:
        return sum(self.ratings.values())


@dataclass
class Rule:
    condition: str
    target: str


class Workflow:
    rules: list[Rule]
    default: str

    def __init__(self,
                 input_str: str):
        rules_str_list = input_str.split(",")
        self.rules = [Rule(*rule_str.split(":")) for rule_str in rules_str_list[:-1]]
        self.default = rules_str_list[-1]

    def apply(self,
              part: Part) -> str:
        for rule in self.rules:
            condition_with_rating = str(part.ratings[rule.condition[0]]) + rule.condition[1:]
            if eval(condition_with_rating):
                return rule.target
        return self.default


class RuleEngine:
    workflows_by_name: dict[str, Workflow]

    def __init__(self,
                 rules_input: str):
        self.workflows_by_name = {}
        for line in rules_input.split("\n"):
            name, second_part = line.split("{")
            self.workflows_by_name[name] = Workflow(second_part[:-1])

    def is_part_accepted(self,
                         part: Part) -> bool:
        workflow = self.workflows_by_name["in"]
        while True:
            workflow_result = workflow.apply(part)
            if workflow_result == "A":
                return True
            if workflow_result == "R":
                return False
            workflow = self.workflows_by_name[workflow_result]


def compute_accepted_parts_rating_sum(lines: list[str]) -> int:
    input_string = "\n".join(lines)
    rules_input, parts_input = input_string.split("\n\n")
    rule_engine = RuleEngine(rules_input)
    parts = (Part(part_string) for part_string in parts_input.split("\n"))
    return sum(part.get_ratings_sum() for part in parts if rule_engine.is_part_accepted(part))
