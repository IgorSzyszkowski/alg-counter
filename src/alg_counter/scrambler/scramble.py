from alg_counter.model.cube import Cube
from dataclasses import dataclass


@dataclass
class Scramble:
    """
    Represents a scramble that schould be used to scramble the cube.
    """
    scramble: str

    def __post_init__(self):
        """
        Checks wheter the scramble is valid

        Raises:
            ValueError: if the scramble is invalid
        """
        scramble_list = self.decode_scramble()
        all_moves = list()
        for move in ["R", "L", "U", "D", "F", "B"]:
            all_moves.extend([move, move + "'", move + "2"])
        if not all([(move in all_moves) for move in scramble_list]):
            raise ValueError("Invalid scramble")

    def decode_scramble(self) -> list[str]:
        scramble_list = self.scramble.strip().split(" ")
        return scramble_list

    def scramble_cube(self, cube: Cube) -> None:
        scramble_list = self.decode_scramble()
        for move in scramble_list:
            cube.apply_move(move)