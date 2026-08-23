"""
Module for parsing, validating, and generating Rubik's Cube scrambles.
"""

import random
from dataclasses import dataclass

from alg_counter.model.cube import Cube


@dataclass
class Scramble:
    """Represents a sequence of moves used to scramble a Rubik's Cube.

    Attributes:
        scramble (str): A string containing WCA-compliant moves separated by spaces.
    """

    scramble: str

    def __post_init__(self) -> None:
        """Checks whether the provided scramble string is valid.

        Raises:
            ValueError: If the scramble contains invalid or unsupported moves.
        """
        scramble_list = self.decode_scramble()
        all_moves = []
        for move in ["R", "L", "U", "D", "F", "B"]:
            all_moves.extend(
                [move, move + "'", move + "2", move + "w", move + "w'", move + "w2"]
            )
        if not all(move in all_moves for move in scramble_list):
            raise ValueError("Invalid scramble")

    def decode_scramble(self) -> list[str]:
        """Splits the scramble string into a list of individual moves.

        Returns:
            list[str]: A list containing each move as a separate string.
        """
        # split() without arguments safely handles multiple consecutive spaces
        scramble_list = self.scramble.strip().split()
        return scramble_list

    def scramble_cube(self, cube: Cube) -> None:
        """Applies the parsed scramble moves to a given Cube instance.

        Args:
            cube (Cube): The cube instance to be scrambled.
        """
        scramble_list = self.decode_scramble()
        for move in scramble_list:
            cube.apply_move(move)

    @staticmethod
    def get_wca_scramble(length: int = 20) -> str:
        """Generates a random, WCA-compliant scramble.

        Ensures that consecutive moves do not turn the same face, and avoids
        redundant sequences like turning opposite faces consecutively and then
        returning to the original face (e.g., prevents "R L R").

        Args:
            length (int, optional): The number of moves in the scramble. Defaults to 20.

        Returns:
            str: A randomly generated scramble string.
        """
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
