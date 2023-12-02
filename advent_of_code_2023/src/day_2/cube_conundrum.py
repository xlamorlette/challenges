from enum import Enum
from typing import Dict, List


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


ALL_COLORS: List[Color] = [Color.RED, Color.GREEN, Color.BLUE]

COLOR_PER_STRING: Dict[str, Color] = {
    "red": Color.RED,
    "green": Color.GREEN,
    "blue": Color.BLUE
}


CubesCombination = Dict[Color, int]


NB_CUBES_PER_COLOR_IN_BAG: CubesCombination = {
    Color.RED: 12,
    Color.GREEN: 13,
    Color.BLUE: 14
}


class Game:
    id: int
    draws: List[CubesCombination]

    def __init__(self,
                 line: str):
        self.id = self._get_game_id(line)
        self.draws = self._get_draws(line)

    @staticmethod
    def _get_game_id(line: str) -> int:
        game_string = line.split(":")[0]
        return int(game_string.split(" ")[1])

    @classmethod
    def _get_draws(cls,
                   line: str) -> List[CubesCombination]:
        draws_string = line.split(": ")[1]
        draw_string_list = draws_string.split("; ")
        return [cls._get_draw(string) for string in draw_string_list]

    @staticmethod
    def _get_draw(draw_string: str) -> CubesCombination:
        result: CubesCombination = dict((color, 0) for color in ALL_COLORS)
        cube_string_list = draw_string.split(", ")
        for cube_string in cube_string_list:
            number_and_color = cube_string.split(" ")
            number = int(number_and_color[0])
            color = COLOR_PER_STRING[number_and_color[1]]
            result[color] = number
        return result


def is_draw_possible(draw: CubesCombination) -> bool:
    return all(draw[color] <= NB_CUBES_PER_COLOR_IN_BAG[color] for color in ALL_COLORS)


def is_game_possible(game: Game) -> bool:
    return all(is_draw_possible(draw) for draw in game.draws)


def compute_possible_games_ids_sum(lines: List[str]) -> int:
    possible_games_ids_sum: int = 0
    for line in lines:
        game = Game(line)
        if is_game_possible(game):
            possible_games_ids_sum += game.id
    return possible_games_ids_sum
