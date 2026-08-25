"""
Module defining the Rubik's Cube model and its internal state.

Provides the `Cube` class used to simulate cube rotations and track the
positions of edges and corners, which is crucial for algorithms counting (e.g., in BLD solving).
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, NewType

from alg_counter.model.color import Color, to_color

CubeStr = NewType("CubeStr", str)
"""NewType representing the cube state as a 54-character string."""

SOLVED_CUBE = CubeStr("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")

Corner = NewType("Corner", tuple[tuple[Color, Color, Color], tuple[int, int, int]])
"""NewType representing a corner's colors and its corresponding indices on the cube string."""

Edge = NewType("Edge", tuple[tuple[Color, Color], tuple[int, int]])
"""NewType representing an edge's colors and its corresponding indices on the cube string."""

solved_corners = [
    Corner(((Color.U, Color.R, Color.F), (8, 9, 20))),
    Corner(((Color.U, Color.B, Color.R), (2, 45, 11))),
    Corner(((Color.U, Color.L, Color.B), (0, 36, 47))),
    Corner(((Color.U, Color.F, Color.L), (6, 18, 38))),
    Corner(((Color.R, Color.D, Color.F), (15, 29, 26))),
    Corner(((Color.L, Color.F, Color.D), (44, 24, 27))),
    Corner(((Color.R, Color.B, Color.D), (17, 51, 35))),
    Corner(((Color.L, Color.D, Color.B), (42, 33, 53))),
]

solved_edges = [
    Edge(((Color.U, Color.F), (7, 19))),
    Edge(((Color.U, Color.R), (5, 10))),
    Edge(((Color.U, Color.L), (3, 37))),
    Edge(((Color.U, Color.B), (1, 46))),
    Edge(((Color.R, Color.F), (12, 23))),
    Edge(((Color.L, Color.F), (41, 21))),
    Edge(((Color.R, Color.D), (16, 32))),
    Edge(((Color.L, Color.D), (43, 30))),
    Edge(((Color.R, Color.B), (14, 48))),
    Edge(((Color.L, Color.B), (39, 50))),
    Edge(((Color.F, Color.D), (25, 28))),
    Edge(((Color.B, Color.D), (52, 34))),
]

orientation_transition = {
    "x": {
        "L": "L",
        "R": "R",
        "U": "F",
        "F": "D",
        "D": "B",
        "B": "U",
    },
    "z": {
        "F": "F",
        "B": "B",
        "U": "L",
        "D": "R",
        "R": "U",
        "L": "D",
    },
    "y": {
        "U": "U",
        "D": "D",
        "R": "B",
        "L": "F",
        "F": "R",
        "B": "L",
    },
}


@dataclass
class Cube:
    """Represents the physical state and mechanics of a Rubik's Cube.

    Attributes:
        cube (CubeStr): A 54-character string representing the color configuration
            of all faces (Up, Right, Front, Down, Left, Back). Each face
            lists its 9 elements row by row, starting from the top-left corner.
            Defaults to a fully solved cube state.
    """

    cube: CubeStr = field(default=SOLVED_CUBE)

    moves_transition: dict[str, str] = field(init=False)
    _physical: dict[str, Callable[[], Any]] = field(init=False)
    moves_dict: dict[str, Callable[[], Any]] = field(init=False)
    solved_corners: list = field(init=False)
    solved_edges: list = field(init=False)

    def __post_init__(self):
        """Initializes movement mappings and instance-specific solved states."""
        self._physical = {
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
        self.moves_transition = {
            "R": "R",
            "U": "U",
            "L": "L",
            "F": "F",
            "B": "B",
            "D": "D",
        }
        self.moves_dict = {
            "U": lambda: self._execute_mapped("U"),
            "U'": lambda: self._execute_mapped("U'"),
            "U2": lambda: self._execute_mapped("U2"),
            "R": lambda: self._execute_mapped("R"),
            "R'": lambda: self._execute_mapped("R'"),
            "R2": lambda: self._execute_mapped("R2"),
            "L": lambda: self._execute_mapped("L"),
            "L'": lambda: self._execute_mapped("L'"),
            "L2": lambda: self._execute_mapped("L2"),
            "D": lambda: self._execute_mapped("D"),
            "D'": lambda: self._execute_mapped("D'"),
            "D2": lambda: self._execute_mapped("D2"),
            "F": lambda: self._execute_mapped("F"),
            "F'": lambda: self._execute_mapped("F'"),
            "F2": lambda: self._execute_mapped("F2"),
            "B": lambda: self._execute_mapped("B"),
            "B'": lambda: self._execute_mapped("B'"),
            "B2": lambda: self._execute_mapped("B2"),
            "x": lambda: self._rotate("x"),
            "x'": lambda: self._rotate("x'"),
            "x2": lambda: self._rotate("x2"),
            "y": lambda: self._rotate("y"),
            "y'": lambda: self._rotate("y'"),
            "y2": lambda: self._rotate("y2"),
            "z": lambda: self._rotate("z"),
            "z'": lambda: self._rotate("z'"),
            "z2": lambda: self._rotate("z2"),
            "Rw": lambda: [self._execute_mapped("L"), self._rotate("x")],
            "Rw'": lambda: [self._execute_mapped("L'"), self._rotate("x'")],
            "Rw2": lambda: [self._execute_mapped("L2"), self._rotate("x2")],
            "Lw": lambda: [self._execute_mapped("R"), self._rotate("x'")],
            "Lw'": lambda: [self._execute_mapped("R'"), self._rotate("x")],
            "Lw2": lambda: [self._execute_mapped("R2"), self._rotate("x2")],
            "Uw": lambda: [self._execute_mapped("D"), self._rotate("y")],
            "Uw'": lambda: [self._execute_mapped("D'"), self._rotate("y'")],
            "Uw2": lambda: [self._execute_mapped("D2"), self._rotate("y2")],
            "Dw": lambda: [self._execute_mapped("U"), self._rotate("y'")],
            "Dw'": lambda: [self._execute_mapped("U'"), self._rotate("y")],
            "Dw2": lambda: [self._execute_mapped("U2"), self._rotate("y2")],
            "Fw": lambda: [self._execute_mapped("B"), self._rotate("z")],
            "Fw'": lambda: [self._execute_mapped("B'"), self._rotate("z'")],
            "Fw2": lambda: [self._execute_mapped("B2"), self._rotate("z2")],
            "Bw": lambda: [self._execute_mapped("F"), self._rotate("z'")],
            "Bw'": lambda: [self._execute_mapped("F'"), self._rotate("z")],
            "Bw2": lambda: [self._execute_mapped("F2"), self._rotate("z2")],
        }

    def _execute_mapped(self, move: str) -> None:
        """Tłumaczy ruch (np. U, F', R2) bazując na aktualnej orientacji kostki i go wykonuje."""
        base_face = move[0]
        modifier = move[1:] if len(move) > 1 else ""

        physical_face = self.moves_transition[base_face]

        self._physical[physical_face + modifier]()

    def _rotate(self, rot: str) -> None:
        """Aktualizuje słownik moves_transition w oparciu o rotację."""
        axis = rot[0]
        modifier = rot[1:] if len(rot) > 1 else ""

        if modifier == "'":
            times = 3
        elif modifier == "2":
            times = 2
        else:
            times = 1

        for _ in range(times):
            new_transition = {}
            for logical_face in self.moves_transition:
                new_transition[logical_face] = self.moves_transition[
                    orientation_transition[axis][logical_face]
                ]
            self.moves_transition = new_transition

    def _rotate_face(self, start: int) -> None:
        """Rotates a single 9-element face 90 degrees clockwise."""
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
        """Applies a U (Up) move."""
        self._rotate_face(0)
        c = list(self.cube)
        temp = c[18:21]
        c[18:21] = c[9:12]
        c[9:12] = c[45:48]
        c[45:48] = c[36:39]
        c[36:39] = temp
        self.cube = CubeStr("".join(c))

    def _d(self) -> None:
        """Applies a D (Down) move."""
        self._rotate_face(27)
        c = list(self.cube)
        temp = c[24:27]
        c[24:27] = c[42:45]
        c[42:45] = c[51:54]
        c[51:54] = c[15:18]
        c[15:18] = temp
        self.cube = CubeStr("".join(c))

    def _l(self) -> None:
        """Applies an L (Left) move."""
        self._rotate_face(36)
        c = list(self.cube)
        temp = [c[0], c[3], c[6]]
        c[0], c[3], c[6] = c[53], c[50], c[47]
        c[53], c[50], c[47] = c[27], c[30], c[33]
        c[27], c[30], c[33] = c[18], c[21], c[24]
        c[18], c[21], c[24] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _r(self) -> None:
        """Applies an R (Right) move."""
        self._rotate_face(9)
        c = list(self.cube)
        temp = [c[2], c[5], c[8]]
        c[2], c[5], c[8] = c[20], c[23], c[26]
        c[20], c[23], c[26] = c[29], c[32], c[35]
        c[29], c[32], c[35] = c[51], c[48], c[45]
        c[51], c[48], c[45] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _f(self) -> None:
        """Applies an F (Front) move."""
        self._rotate_face(18)
        c = list(self.cube)
        temp = [c[6], c[7], c[8]]
        c[6], c[7], c[8] = c[44], c[41], c[38]
        c[44], c[41], c[38] = c[29], c[28], c[27]
        c[29], c[28], c[27] = c[9], c[12], c[15]
        c[9], c[12], c[15] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def _b(self) -> None:
        """Applies a B (Back) move."""
        self._rotate_face(45)
        c = list(self.cube)
        temp = [c[0], c[1], c[2]]
        c[0], c[1], c[2] = c[11], c[14], c[17]
        c[11], c[14], c[17] = c[35], c[34], c[33]
        c[35], c[34], c[33] = c[42], c[39], c[36]
        c[42], c[39], c[36] = temp[0], temp[1], temp[2]
        self.cube = CubeStr("".join(c))

    def apply_move(self, move: str) -> None:
        """Applies a specific move to the cube based on WCA notation.

        Args:
            move (str): A standard Rubik's Cube move (e.g., "U", "R'", "F2").

        Raises:
            ValueError: If the provided move string is not supported or invalid.
        """
        if move in self.moves_dict:
            self.moves_dict[move]()
        else:
            raise ValueError(f"invalid move: {move}")

    def __str__(self) -> str:
        """Returns a string representation of the cube, formatted face by face.

        Returns:
            str: Six lines of text, where each line represents a 9-element face.
        """
        cube_to_string = ""
        for i in range(6):
            cube_to_string += self.cube[i * 9 : 9 + i * 9] + "\n"
        return cube_to_string.strip()

    def adjust_for_parity(self) -> None:
        """Adjusts the internal edge mapping to account for parity.

        Swaps the positions of the UF (Up-Front) and UR (Up-Right) edges
        in the `solved_edges` list to correctly simulate solving behavior
        when the scramble has an odd number of corner targets (parity).
        """
        colors_0, coords_0 = self.solved_edges[0]
        colors_1, coords_1 = self.solved_edges[1]

        self.solved_edges[0] = (colors_1, coords_0)
        self.solved_edges[1] = (colors_0, coords_1)

    def get_current_corners(self) -> dict[tuple[int, int, int], tuple[int, int, int]]:
        """Maps original corner positions to their current positions on the scrambled cube.

        Returns:
            dict[tuple[int, int, int], tuple[int, int, int]]: A dictionary where the key
                is the original (solved) coordinate tuple of the corner, and the value
                is its current coordinate tuple, accounting for orientation (twist).
        """
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
                    break
        return result_dict

    def get_current_edges(self) -> dict[tuple[int, int], tuple[int, int]]:
        """Maps original edge positions to their current positions on the scrambled cube.

        Returns:
            dict[tuple[int, int], tuple[int, int]]: A dictionary where the key
                is the original (solved) coordinate tuple of the edge, and the value
                is its current coordinate tuple, accounting for orientation (flip).
        """
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
                    break
        return result_dict
