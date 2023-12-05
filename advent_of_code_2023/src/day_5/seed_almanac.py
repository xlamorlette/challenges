from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


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


@dataclass
class Range:
    start: int
    length: int

    def end(self) -> int:
        return self.start + self.length - 1

    def intersection(self,
                     other: Range) -> Optional[Range]:
        lower_bound = max(self.start, other.start)
        upper_bound = min(self.end(), other.end())
        if lower_bound > upper_bound:
            return None
        return Range(lower_bound, upper_bound - lower_bound + 1)

    def minus(self,
              other: Range) -> List[Range]:
        result: List[Range] = []
        if self.start < other.start:
            result.append(Range(self.start, other.start - self.start))
        if self.end() > other.end():
            result.append(Range(other.end() + 1, self.end() - other.end()))
        return result


class SeedAlmanac2(SeedAlmanac):
    seed_ranges: List[Range]

    def __init__(self,
                 input_lines: List[str]):
        super().__init__(input_lines)
        self.seed_ranges = [Range(self.seeds[index], self.seeds[index + 1])
                            for index in range(0, len(self.seeds), 2)]

    def compute_lowest_location(self) -> int:
        entity_ranges: List[Range] = self.seed_ranges
        for map_name in MapName:
            # entity_ranges = sum([self.get_destination_ranges(map_name, range_) for range_ in entity_ranges], [])
            entity_ranges = self.get_destination_ranges_without_recursion(map_name, entity_ranges)
        return min(range_.start for range_ in entity_ranges)

    def get_destination_ranges(self,
                               map_name: MapName,
                               entity_range: Range) -> List[Range]:
        map_: Map = self.maps[map_name.value]
        for line in map_:
            intersection: Optional[Range] = entity_range.intersection(Range(line.source_range_start, line.range_length))
            if intersection:
                return [Range(line.destination_range_start + intersection.start - line.source_range_start,
                              intersection.length)] \
                       + sum([self.get_destination_ranges(map_name, range_)
                              for range_ in entity_range.minus(intersection)], [])
        return [entity_range]

    def get_destination_ranges_without_recursion(self,
                                                 map_name: MapName,
                                                 entity_ranges: List[Range]) -> List[Range]:
        result_ranges: List[Range] = []
        map_: Map = self.maps[map_name.value]
        for range_ in entity_ranges:
            for line in map_:
                intersection: Optional[Range] = range_.intersection(Range(line.source_range_start, line.range_length))
                if intersection:
                    result_ranges.append(Range(line.destination_range_start + intersection.start
                                               - line.source_range_start, intersection.length))
                    entity_ranges += range_.minus(intersection)
                    break
            else:
                result_ranges.append(range_)
        return result_ranges
