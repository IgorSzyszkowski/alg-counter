import random
from dataclasses import dataclass

from alg_counter.model.cube import Cube


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
        all_moves = []
        for move in ["R", "L", "U", "D", "F", "B"]:
            all_moves.extend([move, move + "'", move + "2"])
        if not all(move in all_moves for move in scramble_list):
            raise ValueError("Invalid scramble")

    def decode_scramble(self) -> list[str]:
        scramble_list = self.scramble.strip().split(" ")
        return scramble_list

    def scramble_cube(self, cube: Cube) -> None:
        scramble_list = self.decode_scramble()
        for move in scramble_list:
            cube.apply_move(move)

    @staticmethod
    def get_wca_scramble(length: int = 20) -> str:
        faces = ["U", "D", "L", "R", "F", "B"]
        mods = ["", "'", "2"]
        scramble = []

        opposites = {"U": "D", "D": "U", "L": "R", "R": "L", "F": "B", "B": "F"}

        last_face = None
        prev_face = None

        for _ in range(length):
            available = list(faces)

            if last_face is not None:
                available.remove(last_face)

            if (
                prev_face is not None
                and last_face == opposites.get(prev_face)
                and prev_face in available
            ):
                available.remove(prev_face)

            face = random.choice(available)
            mod = random.choice(mods)
            scramble.append(f"{face}{mod}")

            prev_face = last_face
            last_face = face

        return " ".join(scramble)
