from typing import Final, List

from src.day_5.seed_almanac import MapName, SeedAlmanac, MapLine

INPUT: Final[str] = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

INPUT_LINES: Final[List[str]] = INPUT.split("\n")


def test_compute_lowest_location():
    almanac = SeedAlmanac(INPUT_LINES)
    assert almanac.compute_lowest_location() == 35


def test_get_location_from_seed():
    almanac = SeedAlmanac(INPUT_LINES)
    assert almanac.get_location_from_seed(79) == 82
    assert almanac.get_location_from_seed(14) == 43
    assert almanac.get_location_from_seed(55) == 86
    assert almanac.get_location_from_seed(13) == 35


def test_get_destination_number():
    almanac = SeedAlmanac(INPUT_LINES)
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 0) == 0
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 49) == 49
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 50) == 52
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 97) == 99
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 98) == 50
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 99) == 51
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 100) == 100
    assert almanac.get_destination_number(MapName.SEED_TO_SOIL, 79) == 81
    assert almanac.get_destination_number(MapName.SOIL_TO_FERTILIZER, 81) == 81
    assert almanac.get_destination_number(MapName.FERTILIZER_TO_WATER, 81) == 81
    assert almanac.get_destination_number(MapName.WATER_TO_LIGHT, 81) == 74
    assert almanac.get_destination_number(MapName.LIGHT_TO_TEMPERATURE, 74) == 78
    assert almanac.get_destination_number(MapName.TEMPERATURE_TO_HUMIDITY, 78) == 78
    assert almanac.get_destination_number(MapName.HUMIDITY_TO_LOCATION, 78) == 82


def test_init():
    almanac = SeedAlmanac(INPUT_LINES)
    assert almanac.seeds == [79, 14, 55, 13]
    assert almanac.maps == [
        [MapLine(50, 98, 2), MapLine(52, 50, 48)],
        [MapLine(0, 15, 37), MapLine(37, 52, 2), MapLine(39, 0, 15)],
        [MapLine(49, 53, 8), MapLine(0, 11, 42), MapLine(42, 0, 7), MapLine(57, 7, 4)],
        [MapLine(88, 18, 7), MapLine(18, 25, 70)],
        [MapLine(45, 77, 23), MapLine(81, 45, 19), MapLine(68, 64, 13)],
        [MapLine(0, 69, 1), MapLine(1, 0, 69)],
        [MapLine(60, 56, 37), MapLine(56, 93, 4)]
    ]
