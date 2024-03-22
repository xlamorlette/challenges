# 35min : Bois 2
# 50min : Bronze 846
# 1h10 : Bronze 822
# 2h : Bronze 815
# 2h30 : Bronze 483
# 2h50 : Bronze 211
# 4h30 : Bronze 221

# TODO:
# Maintain grid step:
#   cell state: empty / unknown / filled
#   start: all cells are unknown
#   each turn:
#     set all filled cells to unknown
#     set all cells seen by pacs to empty
#     fill cells from input
# For each pac, test 4 directions.
#     Handle moves across limits.
#   Evaluate each resulting position:
#     Flood full map
#     while flooding, add cell value divided by distance
#       unknown cell: value 0.5
# Avoid auto-blocking:
#   simulate one turn move
#   take randomly one pac and make it moving opposite direction
# Try to chase unseen pacs:
#   Value for opponent pac that can be eaten
#   Negative value for opponent pac that can eat if no ability to switch
#   add to opponent pac number of turn since last seen
#   keep seen opponent pacs one turn (or two turns)
# don't attack opponent pac that can switch
# attack by switching at the last time
# Handle turn with speed only:
#   What is exactly the input?
#   keep in mind previously targeted pellets


from __future__ import annotations
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Final, Optional


def debug(message: str):
    print(message, file=sys.stderr, flush=True)


@dataclass(frozen=True, order=True)
class Position:
    x: int
    y: int

    def __add__(self,
                other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self,
                other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self,
                factor: int) -> Position:
        return Position(self.x * factor, self.y * factor)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def manhattan_distance(self,
                           other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def opposite(self) -> Position:
        return Position(- self.x, - self.y)

    def crop_to_limits(self,
                       max_position: Position) -> Position:
        x = min(max(0, self.x), max_position.x)
        y = min(max(0, self.y), max_position.y)
        return Position(x=x, y=y)


NIL_POSITION: Final[Position] = Position(0, 0)
NORTH: Final[Position] = Position(0, -1)
EAST: Final[Position] = Position(1, 0)
SOUTH: Final[Position] = Position(0, 1)
WEST: Final[Position] = Position(-1, 0)
ALL_DIRECTIONS: Final[list[Position]] = [NORTH, EAST, SOUTH, WEST]


class Grid:
    width: int = 0
    height: int = 0
    rows: list[str]

    def init_from_input(self):
        self.width, self.height = [int(i) for i in input().split()]
        self.rows = []
        for i in range(self.height):
            row = input()  # one line of the grid: space " " is floor, pound "#" is wall
            self.rows.append(row)

    def get_max_position(self) -> Position:
        return Position(x=self.width - 1, y=self.height - 1)


@dataclass(frozen=True, order=True)
class Pac:
    pac_id: int = 0
    mine: bool = True
    position: Position = NIL_POSITION
    type_id: str = ""
    speed_turns_left: int = 0
    ability_cooldown: int = 0

    @staticmethod
    def get_pac_from_input() -> Pac:
        inputs = input().split()
        pac_id = int(inputs[0])  # pac number (unique within a team)
        mine = inputs[1] != "0"  # true if this pac is yours
        x = int(inputs[2])
        y = int(inputs[3])
        type_id = inputs[4]
        speed_turns_left = int(inputs[5])
        ability_cooldown = int(inputs[6])
        return Pac(
            pac_id=pac_id,
            mine=mine,
            position=Position(x=x, y=y),
            type_id=type_id,
            speed_turns_left=speed_turns_left,
            ability_cooldown=ability_cooldown
        )

    def does_beat(self,
                  opponent_pac: Pac) -> bool:
        if self.type_id == opponent_pac.type_id:
            return False
        match self.type_id:
            case "ROCK":
                return opponent_pac.type_id == "SCISSORS"
            case "SCISSORS":
                return opponent_pac.type_id == "PAPER"
            case "PAPER":
                return opponent_pac.type_id == "ROCK"
        return False

    def get_beating_type(self) -> str:
        match self.type_id:
            case "ROCK":
                return "PAPER"
            case "SCISSORS":
                return "ROCK"
            case "PAPER":
                return "SCISSORS"
        assert False


@dataclass(frozen=True, order=True)
class Pellet:
    position: Position = NIL_POSITION
    value: int = 0

    @staticmethod
    def get_pellet_from_input() -> Pellet:
        x, y, value = [int(j) for j in input().split()]
        return Pellet(position=Position(x=x, y=y), value=value)


class State:
    my_score: int = 0
    opponent_score: int = 0
    pac_list: list[Pac]
    pellet_list: list[Pellet]

    def init_from_input(self):
        self.my_score, self.opponent_score = [int(i) for i in input().split()]
        visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
        self.pac_list = [Pac.get_pac_from_input() for i in range(visible_pac_count)]
        visible_pellet_count = int(input())  # all pellets in sight
        self.pellet_list = [Pellet.get_pellet_from_input() for i in range(visible_pellet_count)]

    def get_pac_by_id(self,
                      mine: bool,
                      pac_id: int) -> Pac:
        for pac in self.pac_list:
            if pac.mine == mine and pac.pac_id == pac_id:
                return pac
        raise RuntimeError(f"Pac {mine} {pac_id} not found")


@dataclass
class Target:
    pellet: Optional[Pellet] = None
    defend_pac: Optional[Pac] = None
    attack_pac: Optional[Pac] = None


class Solver:
    grid: Grid
    state: State

    def __init__(self,
                 grid: Grid,
                 state: State):
        self.grid = grid
        self.state = state

    def get_moves(self) -> list[str]:
        target_per_pac: dict[Pac, Target] = {
            pac: self.get_target(pac) for pac in self.state.pac_list if pac.mine
        }
        self.solve_common_targets(target_per_pac)
        return self.get_moves_from_targets(target_per_pac)

    def get_target(self,
                   pac: Pac) -> Target:
        target: Target = Target()
        self.look_for_opponent_pacs(pac, target)
        target.pellet = self.find_closest_pellet(pac)
        return target

    def look_for_opponent_pacs(self,
                               pac: Pac,
                               target: Target):
        for opponent_pac in self.state.pac_list:
            if opponent_pac.mine:
                continue
            if opponent_pac.position.manhattan_distance(pac.position) > 6:
                continue
            if opponent_pac.does_beat(pac):
                target.defend_pac = opponent_pac
            elif pac.does_beat(opponent_pac):
                target.attack_pac = opponent_pac

    def find_closest_pellet(self,
                            pac: Pac,
                            excluded_pellets: Optional[list[Pellet]] = None) -> Pellet:
        closest_pellet: Pellet = Pellet()
        shortest_distance: float = 1000.0
        for pellet in self.state.pellet_list:
            if excluded_pellets is not None and pellet in excluded_pellets:
                continue
            distance = float(pac.position.manhattan_distance(pellet.position)) / pellet.value
            if distance < shortest_distance:
                shortest_distance = distance
                closest_pellet = pellet
        return closest_pellet

    def solve_common_targets(self,
                             target_per_pac: dict[Pac, Target]):
        pac_list_per_target_pellet = defaultdict(list)
        for pac, target in target_per_pac.items():
            if target.pellet is not None:
                pellet: Pellet = target.pellet
                pac_list_per_target_pellet[pellet].append(pac)
        targeted_pellets = list(pac_list_per_target_pellet.keys())
        for pellet, pac_list in pac_list_per_target_pellet.items():
            if len(pac_list) > 1:
                shortest_distance: float = 1000.0
                for pac in pac_list:
                    distance = float(pellet.position.manhattan_distance(pac.position)) \
                        + (float(pac.pac_id) / 10)
                    shortest_distance = min(shortest_distance, distance)
                for pac in pac_list:
                    distance = float(pellet.position.manhattan_distance(pac.position)) \
                        + (float(pac.pac_id) / 10)
                    if distance > shortest_distance:
                        target_per_pac[pac].pellet = self.find_closest_pellet(pac, targeted_pellets)

    def get_moves_from_targets(self,
                               target_per_pac: dict[Pac, Target]) -> list[str]:
        return [self.get_pac_action(pac, target) for pac, target in target_per_pac.items()]

    def get_pac_action(self,
                       pac: Pac,
                       target: Target) -> str:
        if target.defend_pac is not None:
            action: Optional[str] = self.get_defend_action(pac, target.defend_pac)
            if action is not None:
                return action
        if target.attack_pac is not None:
            action = self.get_attack_action(pac, target.attack_pac)
            if action is not None:
                return action
        assert target.pellet is not None
        return f"MOVE {pac.pac_id} {target.pellet.position.x} {target.pellet.position.y}" \
               + f" miam {target.pellet.position}"

    def get_defend_action(self,
                          pac: Pac,
                          defend_pac: Pac) -> Optional[str]:
        if pac.ability_cooldown == 0:
            new_type_id: str = defend_pac.get_beating_type()
            return f"SWITCH {pac.pac_id} {new_type_id} switch to defend against {defend_pac.pac_id}"
        # TODO: rather find the direction that maximise the distance with defend_pac
        delta_position: Position = defend_pac.position - pac.position
        target_position: Position = pac.position - delta_position
        target_position = target_position.crop_to_limits(self.grid.get_max_position())
        return f"MOVE {pac.pac_id} {target_position.x} {target_position.y}" \
               + f" run away from {defend_pac.pac_id}"

    @staticmethod
    def get_attack_action(pac: Pac,
                          attack_pac: Pac) -> Optional[str]:
        distance: int = pac.position.manhattan_distance(attack_pac.position)
        if 1 < distance and pac.ability_cooldown == 0:
            return f"SPEED {pac.pac_id} rush to attack {attack_pac.pac_id}"
        if distance <= 2 or pac.speed_turns_left > 0:
            return f"MOVE {pac.pac_id} {attack_pac.position.x} {attack_pac.position.y}" \
                   + f" attack {attack_pac.pac_id}"
        return None


def main():
    grid: Grid = Grid()
    grid.init_from_input()
    while True:
        state: State = State()
        state.init_from_input()
        solver: Solver = Solver(grid, state)
        moves: list[str] = solver.get_moves()
        concatenated_moves = " | ".join(moves)
        print(concatenated_moves)


if __name__ == '__main__':
    main()
