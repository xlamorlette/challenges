from dataclasses import dataclass
import math


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


RatingRange = dict[str, range]


def get_rating_range_nb_combinations(rating_range: RatingRange) -> int:
    return math.prod(interval.stop - interval.start for _category, interval in rating_range.items())


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

    def get_ranges_per_target(self,
                              current_rating_range: RatingRange) -> list[tuple[str, RatingRange]]:
        ranges_per_target: list[tuple[str, RatingRange]] = []
        for rule in self.rules:
            rule_category = rule.condition[0]
            comparator = rule.condition[1]
            rule_value = int(rule.condition[2:])
            current_range: range = current_rating_range[rule_category]
            matching_range: range
            non_matching_range: range
            if comparator == "<":
                matching_range = range(current_range.start, min(current_range.stop, rule_value))
                non_matching_range = range(rule_value, current_range.stop)
            else:
                matching_range = range(rule_value + 1, current_range.stop)
                non_matching_range = range(current_range.start, min(current_range.stop, rule_value + 1))
            if matching_range.start < matching_range.stop:
                matching_rating_range: RatingRange = {category: interval
                                                      for category, interval in current_rating_range.items()
                                                      if category != rule_category}
                matching_rating_range[rule_category] = matching_range
                ranges_per_target.append((rule.target, matching_rating_range))
            current_rating_range[rule_category] = non_matching_range
            if non_matching_range.start >= non_matching_range.stop:
                break
        if all(interval.start < interval.stop for _category, interval in current_rating_range.items()):
            ranges_per_target.append((self.default, current_rating_range))
        return ranges_per_target


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

    def get_total_nb_accepted_combinations(self,
                                           rating_range: RatingRange) -> int:
        return self.get_nb_accepted_combinations(rating_range, "in")

    def get_nb_accepted_combinations(self,
                                     input_rating_range: RatingRange,
                                     workflow_name: str) -> int:
        workflow: Workflow = self.workflows_by_name[workflow_name]
        ranges_per_target: list[tuple[str, RatingRange]] = workflow.get_ranges_per_target(input_rating_range)
        nb_accepted_combinations: int = 0
        for target, rating_range in ranges_per_target:
            if target == "A":
                nb_accepted_combinations += get_rating_range_nb_combinations(rating_range)
            elif target != "R":
                nb_accepted_combinations += self.get_nb_accepted_combinations(rating_range, target)
        return nb_accepted_combinations


def compute_accepted_parts_rating_sum(lines: list[str]) -> int:
    input_string = "\n".join(lines)
    rules_input, parts_input = input_string.split("\n\n")
    rule_engine = RuleEngine(rules_input)
    parts = (Part(part_string) for part_string in parts_input.split("\n"))
    return sum(part.get_ratings_sum() for part in parts if rule_engine.is_part_accepted(part))


def compute_number_of_accepted_combinations(lines: list[str]) -> int:
    input_string = "\n".join(lines)
    rules_input, _parts_input = input_string.split("\n\n")
    rating_range: RatingRange = {category: range(1, 4001) for category in "xmas"}
    return RuleEngine(rules_input).get_total_nb_accepted_combinations(rating_range)
