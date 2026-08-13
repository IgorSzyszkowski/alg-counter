from dataclasses import dataclass, field
from typing import Final, NewType


cube_str = NewType("cube_str", str)
"""
new type representing cube as string
"""

SOLVED_CUBE = cube_str("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")


@dataclass
class Cube:
    """Represents the state of a Rubik's Cube.

    Attributes:
        cube (str): A 54-character string representing the color configuration
                    of all faces (Up, Right, Front, Down, Left, Back). Each face
                    lists its 9 elements row by row, starting from the top-left corner.
                    Defaults to a fully solved cube state.
    """

    cube: cube_str = field(default=SOLVED_CUBE)

    def __post_init__(self):
        self.moves_dict = {
            "U": lambda: self._u(),
            "U'": lambda: [self._u() for _ in range(3)],
            "U2": lambda: [self._u() for _ in range(2)],
            "R": lambda: self._r(),
            "R'": lambda: [self._r() for _ in range(3)],
            "R2": lambda: [self._r() for _ in range(2)],
            "L": lambda: self._l(),
            "L'": lambda: [self._l() for _ in range(3)],
            "L2": lambda: [self._l() for _ in range(2)],
            "D": lambda: self._d(),
            "D'": lambda: [self._d() for _ in range(3)],
            "D2": lambda: [self._d() for _ in range(2)],
            "F": lambda: self._f(),
            "F'": lambda: [self._f() for _ in range(3)],
            "F2": lambda: [self._f() for _ in range(2)],
            "B": lambda: self._b(),
            "B'": lambda: [self._b() for _ in range(3)],
            "B2": lambda: [self._b() for _ in range(2)],
        }

    def _rotate_face(self, start: int) -> None:
        chars = list(self.cube)
        face = chars[start : start + 9]
        chars[start : start + 9] = [
            face[6],
            face[3],
            face[0],
            face[7],
            face[4],
            face[1],
            face[8],
            face[5],
            face[2],
        ]
        self.cube = "".join(chars)

    def _u(self) -> None:
        self._rotate_face(0)
        c = list(self.cube)
        temp = c[18:21]
        c[18:21] = c[9:12]
        c[9:12] = c[45:48]
        c[45:48] = c[36:39]
        c[36:39] = temp
        self.cube = "".join(c)

    def _d(self) -> None:
        self._rotate_face(27)
        c = list(self.cube)
        temp = c[24:27]
        c[24:27] = c[42:45]
        c[42:45] = c[51:54]
        c[51:54] = c[15:18]
        c[15:18] = temp
        self.cube = "".join(c)

    def _l(self) -> None:
        self._rotate_face(36)
        c = list(self.cube)
        temp = [c[0], c[3], c[6]]
        c[0], c[3], c[6] = c[53], c[50], c[47]
        c[53], c[50], c[47] = c[27], c[30], c[33]
        c[27], c[30], c[33] = c[18], c[21], c[24]
        c[18], c[21], c[24] = temp[0], temp[1], temp[2]
        self.cube = "".join(c)

    def _r(self) -> None:
        self._rotate_face(9)
        c = list(self.cube)
        temp = [c[2], c[5], c[8]]
        c[2], c[5], c[8] = c[20], c[23], c[26]
        c[20], c[23], c[26] = c[29], c[32], c[35]
        c[29], c[32], c[35] = c[51], c[48], c[45]
        c[51], c[48], c[45] = temp[0], temp[1], temp[2]
        self.cube = "".join(c)

    def _f(self) -> None:
        self._rotate_face(18)
        c = list(self.cube)
        temp = [c[6], c[7], c[8]]
        c[6], c[7], c[8] = c[44], c[41], c[38]
        c[44], c[41], c[38] = c[29], c[28], c[27]
        c[29], c[28], c[27] = c[9], c[12], c[15]
        c[9], c[12], c[15] = temp[0], temp[1], temp[2]
        self.cube = "".join(c)

    def _b(self) -> None:
        self._rotate_face(45)
        c = list(self.cube)
        temp = [c[0], c[1], c[2]]
        c[0], c[1], c[2] = c[11], c[14], c[17]
        c[11], c[14], c[17] = c[35], c[34], c[33]
        c[35], c[34], c[33] = c[42], c[39], c[36]
        c[42], c[39], c[36] = temp[0], temp[1], temp[2]
        self.cube = "".join(c)

    def apply_move(self, move: str) -> None:
        if move in self.moves_dict:
            self.moves_dict[move]()
        else:
            raise ValueError(f"invalid move: {move}")

    def __str__(self) -> str:
        cube_to_string = ""
        for i in range(6):
            cube_to_string += self.cube[i * 9: 9 + i * 9] + "\n"
        return cube_to_string.strip()
