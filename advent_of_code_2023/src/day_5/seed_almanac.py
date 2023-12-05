from dataclasses import dataclass
from enum import Enum
from typing import List


class MapName(Enum):
    SEED_TO_SOIL = 0
    SOIL_TO_FERTILIZER = 1
    FERTILIZER_TO_WATER = 2
    WATER_TO_LIGHT = 3
    LIGHT_TO_TEMPERATURE = 4
    TEMPERATURE_TO_HUMIDITY = 5
    HUMIDITY_TO_LOCATION = 6


@dataclass
class MapLine:
    destination_range_start: int
    source_range_start: int
    range_length: int


Map = List[MapLine]


class SeedAlmanac:
    seeds: List[int]
    maps: List[Map]

    def __init__(self,
                 input_lines: List[str]):
        self.seeds = list(map(int, input_lines[0].split(":")[1].split()))
        self.maps = []
        for line in input_lines[1:]:
            if line == "":
                continue
            if line.endswith(":"):
                self.maps.append([])
                continue
            numbers: List[int] = list(map(int, line.split()))
            self.maps[-1].append(MapLine(*numbers))

    def compute_lowest_location(self) -> int:
        return min(map(self.get_location_from_seed, self.seeds))

    def get_location_from_seed(self,
                               seed: int) -> int:
        entity_number = seed
        for map_name in MapName:
            entity_number = self.get_destination_number(map_name, entity_number)
        return entity_number

    def get_destination_number(self,
                               map_name: MapName,
                               source_number: int) -> int:
        map_: Map = self.maps[map_name.value]
        for line in map_:
            if line.source_range_start <= source_number < line.source_range_start + line.range_length:
                return line.destination_range_start + source_number - line.source_range_start
        return source_number
