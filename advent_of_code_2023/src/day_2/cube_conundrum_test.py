from typing import Final, List

from src.day_2.cube_conundrum import Color, Game, compute_possible_games_ids_sum, compute_power_of_minimum_set, \
    compute_sum_of_power_of_minimum_set, get_minimum_set, is_game_possible


GAMES: Final[List[str]] = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
]


def test_compute_possible_games_ids_sum():
    assert compute_possible_games_ids_sum(GAMES) == 8


def test_game_constructor():
    game = Game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert game.id == 1
    assert game.draws == [
        {Color.RED: 4, Color.GREEN: 0, Color.BLUE: 3},
        {Color.RED: 1, Color.GREEN: 2, Color.BLUE: 6},
        {Color.RED: 0, Color.GREEN: 2, Color.BLUE: 0}
    ]
    game = Game("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red")
    assert game.id == 3
    assert game.draws == [
        {Color.RED: 20, Color.GREEN: 8, Color.BLUE: 6},
        {Color.RED: 4, Color.GREEN: 13, Color.BLUE: 5},
        {Color.RED: 1, Color.GREEN: 5, Color.BLUE: 0}
    ]


def test_is_game_possible():
    assert is_game_possible(Game(GAMES[0]))
    assert not is_game_possible(Game(GAMES[2]))


def test_compute_sum_of_power_of_minimum_set():
    assert compute_sum_of_power_of_minimum_set(GAMES) == 2286


def test_compute_power_of_minimum_set():
    assert compute_power_of_minimum_set(Game(GAMES[0])) == 48
    assert compute_power_of_minimum_set(Game(GAMES[1])) == 12
    assert compute_power_of_minimum_set(Game(GAMES[2])) == 1560
    assert compute_power_of_minimum_set(Game(GAMES[3])) == 630
    assert compute_power_of_minimum_set(Game(GAMES[4])) == 36


def test_get_minimum_set():
    assert get_minimum_set(Game(GAMES[0])) == {Color.RED: 4, Color.GREEN: 2, Color.BLUE: 6}
    assert get_minimum_set(Game(GAMES[1])) == {Color.RED: 1, Color.GREEN: 3, Color.BLUE: 4}
    assert get_minimum_set(Game(GAMES[2])) == {Color.RED: 20, Color.GREEN: 13, Color.BLUE: 6}
    assert get_minimum_set(Game(GAMES[3])) == {Color.RED: 14, Color.GREEN: 3, Color.BLUE: 15}
    assert get_minimum_set(Game(GAMES[4])) == {Color.RED: 6, Color.GREEN: 3, Color.BLUE: 2}
