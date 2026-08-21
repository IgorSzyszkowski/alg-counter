from dataclasses import dataclass, field
from typing import NewType

from alg_counter.model.color import Color, to_color

CubeStr = NewType("CubeStr", str)
"""
new type representing cube as string
"""

SOLVED_CUBE = CubeStr("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")

Corner = NewType("Corner", tuple[tuple[Color, Color, Color], tuple[int, int, int]])

Edge = NewType("Edge", tuple[tuple[Color, Color], tuple[int, int]])

solved_corners = [
    Corner(((Color.U, Color.R, Color.F), (8, 9, 20))),
    Corner(((Color.U, Color.F, Color.L), (6, 18, 38))),
    Corner(((Color.U, Color.L, Color.B), (0, 36, 47))),
    Corner(((Color.U, Color.B, Color.R), (2, 45, 11))),
    Corner(((Color.D, Color.F, Color.R), (29, 26, 15))),
    Corner(((Color.D, Color.L, Color.F), (27, 44, 24))),
    Corner(((Color.D, Color.B, Color.L), (33, 53, 42))),
    Corner(((Color.D, Color.R, Color.B), (35, 17, 51))),
]
solved_edges = [
    Edge(((Color.U, Color.F), (7, 19))),
    Edge(((Color.U, Color.B), (1, 46))),
    Edge(((Color.U, Color.L), (3, 37))),
    Edge(((Color.U, Color.R), (5, 10))),
    Edge(((Color.F, Color.L), (21, 41))),
    Edge(((Color.F, Color.R), (23, 12))),
    Edge(((Color.L, Color.B), (39, 50))),
    Edge(((Color.R, Color.B), (14, 48))),
    Edge(((Color.D, Color.F), (28, 25))),
    Edge(((Color.D, Color.B), (34, 52))),
    Edge(((Color.D, Color.L), (30, 43))),
    Edge(((Color.D, Color.R), (32, 16))),
]


@dataclass
class Cube:
    """Represents the state of a Rubik's Cube.

    Attributes:
        cube (str): A 54-character string representing the color configuration
                    of all faces (Up, Right, Front, Down, Left, Back). Each face
                    lists its 9 elements row by row, starting from the top-left corner.
                    Defaults to a fully solved cube state.
    """

    cube: CubeStr = field(default=SOLVED_CUBE)

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
        self.solved_corners = solved_corners.copy()
        self.solved_edges = solved_edges.copy()

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
        self.cube = CubeStr("".join(chars))

    def _u(self) -> None:
        self._rotate_face(0)
        c = list(self.cube)
        temp = c[18:21]
        c[18:21] = c[9:12]
        c[9:12] = c[45:48]
        c[45:48] = c[36:39]
        c[36:39] = temp
        self.cube = CubeStr("".join(c))

    def _d(self) -> None:
        self._rotate_face(27)
        c = list(self.cube)
        temp = c[24:27]
        c[24:27] = c[42:45]
        c[42:45] = c[51:54]
        c[51:54] = c[15:18]
        c[15:18] = temp
        self.cube = CubeStr("".join(c))

    def _l(self) -> None:
        self._rotate_face(36)
        c = list(self.cube)
        temp = [c[0], c[3], c[6]]
        c[0], c[3], c[6] = c[53], c[50], c[47]
        c[53], c[50], c[47] = c[27], c[30], c[33]
        c[27], c[30], c[33] = c[18], c[21], c[24]
        c[18], c[21], c[24] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _r(self) -> None:
        self._rotate_face(9)
        c = list(self.cube)
        temp = [c[2], c[5], c[8]]
        c[2], c[5], c[8] = c[20], c[23], c[26]
        c[20], c[23], c[26] = c[29], c[32], c[35]
        c[29], c[32], c[35] = c[51], c[48], c[45]
        c[51], c[48], c[45] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _f(self) -> None:
        self._rotate_face(18)
        c = list(self.cube)
        temp = [c[6], c[7], c[8]]
        c[6], c[7], c[8] = c[44], c[41], c[38]
        c[44], c[41], c[38] = c[29], c[28], c[27]
        c[29], c[28], c[27] = c[9], c[12], c[15]
        c[9], c[12], c[15] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _b(self) -> None:
        self._rotate_face(45)
        c = list(self.cube)
        temp = [c[0], c[1], c[2]]
        c[0], c[1], c[2] = c[11], c[14], c[17]
        c[11], c[14], c[17] = c[35], c[34], c[33]
        c[35], c[34], c[33] = c[42], c[39], c[36]
        c[42], c[39], c[36] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def apply_move(self, move: str) -> None:
        if move in self.moves_dict:
            self.moves_dict[move]()
        else:
            raise ValueError(f"invalid move: {move}")

    def __str__(self) -> str:
        cube_to_string = ""
        for i in range(6):
            cube_to_string += self.cube[i * 9 : 9 + i * 9] + "\n"
        return cube_to_string.strip()

    def adjust_for_parity(self) -> None:
        colors_0, coords_0 = self.solved_edges[0]
        colors_3, coords_3 = self.solved_edges[3]

        self.solved_edges[0] = (colors_3, coords_0)
        self.solved_edges[3] = (colors_0, coords_3)

    def get_current_corners(self) -> dict[tuple[int, int, int], tuple[int, int, int]]:
        result_dict = {}
        for corner_key in self.solved_corners:
            corner_value = ()
            current_colors = (
                to_color(self.cube[corner_key[1][0]]),
                to_color(self.cube[corner_key[1][1]]),
                to_color(self.cube[corner_key[1][2]]),
            )
            for corner in self.solved_corners:
                if set(current_colors) == set(corner[0]):
                    if current_colors[0] == corner[0][0]:
                        corner_value = corner[1]
                    elif current_colors[0] == corner[0][1]:
                        corner_value = corner[1][1:] + corner[1][0:1]
                    else:
                        corner_value = corner[1][2:3] + corner[1][:2]
            result_dict[corner_key[1]] = corner_value
        return result_dict

    def get_current_edges(self) -> dict[tuple[int, int], tuple[int, int]]:
        result_dict = {}
        for edge_key in self.solved_edges:
            edge_value = ()
            current_colors = (
                to_color(self.cube[edge_key[1][0]]),
                to_color(self.cube[edge_key[1][1]]),
            )
            for edge in self.solved_edges:
                if set(current_colors) == set(edge[0]):
                    if current_colors[0] == edge[0][0]:
                        edge_value = edge[1]
                    else:
                        edge_value = edge[1][1:2] + edge[1][0:1]
            result_dict[edge_key[1]] = edge_value
        return result_dict
