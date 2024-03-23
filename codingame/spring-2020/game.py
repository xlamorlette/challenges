# 35min : Bois 2
# 50min : Bronze 846
# 1h10 : Bronze 822
# 2h30 : Bronze 483
# 3h : Bronze 211
# 8h : Bronze 66
# 8h15 : Argent 664
# 8h30 : Argent 474

# TODO:
# keep seen opponent pacs one turn (or two turns)
# only defensive action against opponent pac that can reach me
# attack by switching at the last time
# Try to chase unseen pacs:
#   Value for opponent pac that can be eaten
#   Negative value for opponent pac that can eat if no ability to switch
#   add to opponent pac number of turn since last seen
# Handle turn with speed only:
#   What is exactly the input?
#   keep in mind previously targeted pellets


from __future__ import annotations
import sys
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
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


class CellState(Enum):
    WALL = 0
    UNKNOWN = 1
    EMPTY = 2
    PELLET = 3
    SUPER_PELLET = 4


STRING_PER_CELL_STATE: Final[dict[CellState, str]] = {
    CellState.WALL: "#",
    CellState.UNKNOWN: ".",
    CellState.EMPTY: " ",
    CellState.PELLET: "+",
    CellState.SUPER_PELLET: "X"
}


class Grid:
    width: int = 0
    height: int = 0
    cells: list[list[CellState]]

    def init_from_input(self):
        self.width, self.height = [int(i) for i in input().split()]
        self.cells = [[CellState.UNKNOWN] * self.width for _row_index in range(self.height)]
        for row in range(self.height):
            row_string = input()  # one line of the grid: space " " is floor, pound "#" is wall
            assert len(row_string) == self.width
            for column in range(self.width):
                match row_string[column]:
                    case ' ':
                        self.cells[row][column] = CellState.UNKNOWN
                    case '#':
                        self.cells[row][column] = CellState.WALL
                    case _:
                        assert False, "wrong value when reading grid"

    def __str__(self):
        return "\n".join(self._row_string(row) for row in range(self.height))

    def _row_string(self,
                    row: int) -> str:
        return "".join(STRING_PER_CELL_STATE[self.cells[row][column]] for column in range(self.width))

    def is_position_valid(self,
                          position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def get_max_position(self) -> Position:
        return Position(x=self.width - 1, y=self.height - 1)

    def get_cell(self,
                 position: Position) -> CellState:
        return self.cells[position.y][position.x]

    def set_cell(self,
                 position: Position,
                 state: CellState):
        assert self.is_position_valid(position)
        self.cells[position.y][position.x] = state

    def get_cell_value(self,
                       position: Position) -> float:
        match self.cells[position.y][position.x]:
            case CellState.PELLET:
                return 1.0
            case CellState.SUPER_PELLET:
                return 10.0
            case CellState.UNKNOWN:
                return 0.5
        return 0.0

    def move(self,
             position: Position,
             direction: Position) -> Optional[Position]:
        # if there is no wall on a border, there is no wall on the opposite side
        result_position = Position(
            (position.x + direction.x) % self.width,
            (position.y + direction.y) % self.height
        )
        if self.get_cell(result_position) == CellState.WALL:
            return None
        return result_position

    def update(self,
               state: State):
        self._set_filled_cells_to_unknown()
        self._clear_cells_seen_by_pacs(state)
        self._fill_seen_pellets(state)

    def _set_filled_cells_to_unknown(self):
        for row in range(self.height):
            for column in range(self.width):
                match self.cells[row][column]:
                    case CellState.PELLET:
                        self.cells[row][column] = CellState.UNKNOWN
                    case CellState.SUPER_PELLET:
                        self.cells[row][column] = CellState.EMPTY

    def _clear_cells_seen_by_pacs(self,
                                  state: State):
        for pac in state.pac_list:
            if pac.mine:
                self.clear_cells_seen_by_pac(pac)

    def clear_cells_seen_by_pac(self,
                                pac: Pac):
        assert pac.mine
        self.cells[pac.position.y][pac.position.x] = CellState.EMPTY
        for direction in ALL_DIRECTIONS:
            position: Position = pac.position
            new_position: Optional[Position] = self.move(position, direction)
            while new_position is not None:
                position = new_position
                # we can loop infinitely if there is a whole traversing line
                if position == pac.position:
                    break
                self.set_cell(position, CellState.EMPTY)
                new_position = self.move(position, direction)

    def _fill_seen_pellets(self,
                           state: State):
        for pellet in state.pellet_list:
            match pellet.value:
                case 1:
                    self.cells[pellet.position.y][pellet.position.x] = CellState.PELLET
                case 10:
                    self.cells[pellet.position.y][pellet.position.x] = CellState.SUPER_PELLET


@dataclass
class Target:
    defend_pac: Optional[Pac] = None
    attack_pac: Optional[Pac] = None
    explore_position: Position = NIL_POSITION


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
        target.explore_position = self.get_best_next_position(pac)
        return target

    def look_for_opponent_pacs(self,
                               pac: Pac,
                               target: Target):
        # TODO: should take the closest defend and closest attacker
        for opponent_pac in self.state.pac_list:
            if opponent_pac.mine:
                continue
            if opponent_pac.position.manhattan_distance(pac.position) > 6:
                continue
            if opponent_pac.does_beat(pac):
                target.defend_pac = opponent_pac
            elif pac.does_beat(opponent_pac) and not self.opponent_can_switch(pac, opponent_pac):
                target.attack_pac = opponent_pac

    @staticmethod
    def opponent_can_switch(pac: Pac,
                            opponent_pac: Pac) -> bool:
        if opponent_pac.ability_cooldown == 0:
            return True
        distance: int = pac.position.manhattan_distance(opponent_pac.position)
        if pac.speed_turns_left > distance / 2:
            distance /= 2
        else:
            distance -= pac.speed_turns_left
        return opponent_pac.ability_cooldown < distance

    def get_best_next_position(self,
                               pac: Pac) -> Position:
        best_position: Position = pac.position
        best_score: float = 0.0
        for direction in ALL_DIRECTIONS:
            position: Optional[Position] = self.grid.move(pac.position, direction)
            if position is not None:
                score = self.evaluate_position(position)
                if score > best_score:
                    best_score = score
                    best_position = position
        return best_position

    def evaluate_position(self,
                          position: Position) -> float:
        score: float = 0.0
        current_positions: list[Position] = [position]
        nb_current_positions = 1
        nb_turns = 1
        is_position_seen: list[list[bool]] = [[False] * self.grid.width for _row in range(self.grid.height)]
        while nb_current_positions > 0:
            next_positions: list[Position] = [NIL_POSITION] * (nb_current_positions * 4)
            nb_next_positions: int = 0
            for index_current_position in range(nb_current_positions):
                current_position = current_positions[index_current_position]
                if is_position_seen[current_position.y][current_position.x]:
                    continue
                is_position_seen[current_position.y][current_position.x] = True
                score += self.grid.get_cell_value(current_position) / float(nb_turns)
                for direction in ALL_DIRECTIONS:
                    next_position: Optional[Position] = self.grid.move(current_position, direction)
                    if next_position is None or is_position_seen[next_position.y][next_position.x]:
                        continue
                    next_positions[nb_next_positions] = next_position
                    nb_next_positions += 1
            nb_turns += 1
            current_positions = next_positions
            nb_current_positions = nb_next_positions
        return score

    def solve_common_targets(self,
                             target_per_pac: dict[Pac, Target]):
        pac_list_per_position = defaultdict(list)
        for pac, target in target_per_pac.items():
            pac_list_per_position[target.explore_position].append(pac)
        for position, pac_list in pac_list_per_position.items():
            nb_pacs = len(pac_list)
            if nb_pacs > 1:
                for pac in pac_list:
                    for direction in ALL_DIRECTIONS:
                        next_position: Optional[Position] = self.grid.move(pac.position, direction)
                        if next_position is not None and next_position != position:
                            target_per_pac[pac].explore_position = next_position
                            nb_pacs -= 1
                            break
                    if nb_pacs <= 1:
                        break

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
        text: str = ""
        match self.grid.get_cell(target.explore_position):
            case CellState.PELLET:
                text = " miam"
            case CellState.SUPER_PELLET:
                text = " MIAM"
        return f"MOVE {pac.pac_id} {target.explore_position.x} {target.explore_position.y}{text}"

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
        grid.update(state)
        solver: Solver = Solver(grid, state)
        moves: list[str] = solver.get_moves()
        concatenated_moves = " | ".join(moves)
        print(concatenated_moves)


if __name__ == '__main__':
    main()
