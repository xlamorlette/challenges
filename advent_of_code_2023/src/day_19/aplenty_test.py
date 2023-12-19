from typing import Final

from src.day_19.aplenty import Part, Workflow, compute_accepted_parts_rating_sum, \
    compute_number_of_accepted_combinations


INPUT: Final[str] = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

INPUT_LINES: Final[list[str]] = INPUT.split("\n")


def test_compute_accepted_parts_rating_sum():
    assert compute_accepted_parts_rating_sum(INPUT_LINES) == 19114


def test_part_get_ratings_sum():
    assert Part("{x=787,m=2655,a=1222,s=2876}").get_ratings_sum() == 7540


def test_workflow_apply():
    assert Workflow("s<1351:px,qqz").apply(Part("{x=787,m=2655,a=1222,s=2876}")) == "qqz"
    assert Workflow("s>2770:qs,m<1801:hdj,R").apply(Part("{x=787,m=2655,a=1222,s=2876}")) == "qs"


def test_compute_number_of_accepted_combinations():
    assert compute_number_of_accepted_combinations(INPUT_LINES) == 167409079868000


def test_workflow_get_ranges_per_target():
    assert Workflow("s<1351:px,qqz").get_ranges_per_target({"x": range(1, 4001), "s": range(1, 4001)}) == [
        ("px", {"x": range(1, 4001), "s": range(1, 1351)}),
        ("qqz", {"x": range(1, 4001), "s": range(1351, 4001)})
    ]
