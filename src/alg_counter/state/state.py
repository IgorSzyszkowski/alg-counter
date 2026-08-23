"""
Module defining the simulation state, including buffers, parity, and cube orientation.
"""

from alg_counter.model.color import Color, to_color
from alg_counter.model.cube import solved_corners, solved_edges

color_transition_dict: dict[tuple[str, str], dict[Color, Color]] = {
    ("W", "G"): {
        Color.U: Color.U,
        Color.R: Color.R,
        Color.L: Color.L,
        Color.D: Color.D,
        Color.F: Color.F,
        Color.B: Color.B,
    },
    ("W", "O"): {
        Color.U: Color.U,
        Color.R: Color.F,
        Color.L: Color.B,
        Color.D: Color.D,
        Color.F: Color.L,
        Color.B: Color.R,
    },
    ("W", "R"): {
        Color.U: Color.U,
        Color.R: Color.B,
        Color.L: Color.F,
        Color.D: Color.D,
        Color.F: Color.R,
        Color.B: Color.L,
    },
    ("W", "B"): {
        Color.U: Color.U,
        Color.R: Color.L,
        Color.L: Color.R,
        Color.D: Color.D,
        Color.F: Color.B,
        Color.B: Color.F,
    },
    ("Y", "G"): {
        Color.U: Color.D,
        Color.R: Color.L,
        Color.L: Color.R,
        Color.D: Color.U,
        Color.F: Color.F,
        Color.B: Color.B,
    },
    ("Y", "O"): {
        Color.U: Color.D,
        Color.R: Color.B,
        Color.L: Color.F,
        Color.D: Color.U,
        Color.F: Color.L,
        Color.B: Color.R,
    },
    ("Y", "R"): {
        Color.U: Color.D,
        Color.R: Color.F,
        Color.L: Color.B,
        Color.D: Color.U,
        Color.F: Color.R,
        Color.B: Color.L,
    },
    ("Y", "B"): {
        Color.U: Color.D,
        Color.R: Color.R,
        Color.L: Color.L,
        Color.D: Color.U,
        Color.F: Color.B,
        Color.B: Color.F,
    },
    ("G", "W"): {
        Color.U: Color.F,
        Color.R: Color.L,
        Color.L: Color.R,
        Color.D: Color.B,
        Color.F: Color.U,
        Color.B: Color.D,
    },
    ("G", "Y"): {
        Color.U: Color.F,
        Color.R: Color.R,
        Color.L: Color.L,
        Color.D: Color.B,
        Color.F: Color.D,
        Color.B: Color.U,
    },
    ("G", "R"): {
        Color.U: Color.F,
        Color.R: Color.U,
        Color.L: Color.D,
        Color.D: Color.B,
        Color.F: Color.R,
        Color.B: Color.L,
    },
    ("G", "O"): {
        Color.U: Color.F,
        Color.R: Color.D,
        Color.L: Color.U,
        Color.D: Color.B,
        Color.F: Color.L,
        Color.B: Color.R,
    },
    ("B", "W"): {
        Color.U: Color.B,
        Color.R: Color.R,
        Color.L: Color.L,
        Color.D: Color.F,
        Color.F: Color.U,
        Color.B: Color.D,
    },
    ("B", "Y"): {
        Color.U: Color.B,
        Color.R: Color.L,
        Color.L: Color.R,
        Color.D: Color.F,
        Color.F: Color.D,
        Color.B: Color.U,
    },
    ("B", "O"): {
        Color.U: Color.B,
        Color.R: Color.U,
        Color.L: Color.D,
        Color.D: Color.F,
        Color.F: Color.L,
        Color.B: Color.R,
    },
    ("B", "R"): {
        Color.U: Color.B,
        Color.R: Color.D,
        Color.L: Color.U,
        Color.D: Color.F,
        Color.F: Color.R,
        Color.B: Color.L,
    },
    ("O", "W"): {
        Color.U: Color.L,
        Color.R: Color.B,
        Color.L: Color.F,
        Color.D: Color.R,
        Color.F: Color.U,
        Color.B: Color.D,
    },
    ("O", "Y"): {
        Color.U: Color.L,
        Color.R: Color.F,
        Color.L: Color.B,
        Color.D: Color.R,
        Color.F: Color.D,
        Color.B: Color.U,
    },
    ("O", "B"): {
        Color.U: Color.L,
        Color.R: Color.D,
        Color.L: Color.U,
        Color.D: Color.R,
        Color.F: Color.B,
        Color.B: Color.F,
    },
    ("O", "G"): {
        Color.U: Color.L,
        Color.R: Color.U,
        Color.L: Color.D,
        Color.D: Color.R,
        Color.F: Color.F,
        Color.B: Color.B,
    },
    ("R", "G"): {
        Color.U: Color.R,
        Color.R: Color.D,
        Color.L: Color.U,
        Color.D: Color.L,
        Color.F: Color.F,
        Color.B: Color.B,
    },
    ("R", "B"): {
        Color.U: Color.R,
        Color.R: Color.U,
        Color.L: Color.D,
        Color.D: Color.L,
        Color.F: Color.B,
        Color.B: Color.F,
    },
    ("R", "W"): {
        Color.U: Color.R,
        Color.R: Color.F,
        Color.L: Color.B,
        Color.D: Color.L,
        Color.F: Color.U,
        Color.B: Color.D,
    },
    ("R", "Y"): {
        Color.U: Color.R,
        Color.R: Color.B,
        Color.L: Color.F,
        Color.D: Color.L,
        Color.F: Color.D,
        Color.B: Color.U,
    },
}


class State:
    corner_buffer: str
    edge_buffer: str
    orientation: tuple[str, str]
    parity: bool = False
    corner_buffer_position: tuple[int, int, int]
    edge_buffer_position: tuple[int, int]

    def __init__(
        self,
        orientation: tuple[str, str] = ("W", "G"),
        corner_buffer: str = "UFR",
        edge_buffer: str = "UF",
    ):
        """Initializes the State object and calculates physical buffer positions.

        Args:
            orientation (tuple[str, str], optional): Starting orientation as
                (top color, front color), e.g. ("W", "G"). Must be one of the
                24 valid adjacent-color combinations. Defaults to ("W", "G").
            corner_buffer (str, optional): Logical corner buffer, three distinct
                face letters (e.g. "UFR"). Defaults to "UFR".
            edge_buffer (str, optional): Logical edge buffer, two distinct face
                letters (e.g. "UF"). Defaults to "UF".

        Raises:
            ValueError: If the orientation is not one of the 24 valid
                (top, front) combinations, or if a buffer is not a real,
                well-formed corner/edge.
        """
        if orientation not in color_transition_dict:
            valid = ", ".join(
                f"{top}{front}" for top, front in sorted(color_transition_dict)
            )
            raise ValueError(
                f"Invalid orientation {orientation!r}. "
                f"Valid (top, front) combinations: {valid}"
            )

        self.orientation = orientation
        self.corner_buffer = corner_buffer
        self.edge_buffer = edge_buffer
        self.get_corner_buffer_position()
        self.get_edge_buffer_position()

    def get_corner_buffer_position(self) -> None:
        """Calculates the physical string indices for the chosen corner buffer.

        Translates the logical corner buffer (e.g., "UFR") into physical indices
        based on the current cube orientation and stores it in `self.corner_buffer_position`.

        Raises:
            ValueError: If the `corner_buffer` string contains an invalid face
                character, isn't exactly 3 distinct letters, or doesn't
                correspond to a real corner (faces must be mutually adjacent).
        """
        upper_buffer = self.corner_buffer.upper()
        if len(upper_buffer) != 3 or len(set(upper_buffer)) != 3:
            raise ValueError(
                f"Corner buffer must be exactly 3 distinct face letters, "
                f"got: {self.corner_buffer!r}"
            )

        current_transition = color_transition_dict[self.orientation]

        transitioned_colors = []
        for letter in self.corner_buffer:
            color_enum = to_color(letter)
            if color_enum is None:
                raise ValueError(f"Invalid face character in corner buffer: {letter}")
            transitioned_colors.append(current_transition[color_enum])

        transitioned_corner_buffer = tuple(transitioned_colors)

        for corner in solved_corners:
            if set(corner[0]) == set(transitioned_corner_buffer):
                if transitioned_corner_buffer[0] == corner[0][0]:
                    self.corner_buffer_position = corner[1]
                elif transitioned_corner_buffer[0] == corner[0][1]:
                    self.corner_buffer_position = corner[1][1:] + corner[1][:1]
                else:
                    self.corner_buffer_position = corner[1][2:] + corner[1][:2]
                return

        raise ValueError(
            f"{self.corner_buffer!r} is not a valid corner "
            f"(the three faces must be mutually adjacent)."
        )

    def get_edge_buffer_position(self) -> None:
        """Calculates the physical string indices for the chosen edge buffer.

        Translates the logical edge buffer (e.g., "UF") into physical indices
        based on the current cube orientation and stores it in `self.edge_buffer_position`.

        Raises:
            ValueError: If the `edge_buffer` string contains an invalid face
                character, isn't exactly 2 distinct letters, or doesn't
                correspond to a real edge (faces must be adjacent).
        """
        upper_buffer = self.edge_buffer.upper()
        if len(upper_buffer) != 2 or len(set(upper_buffer)) != 2:
            raise ValueError(
                f"Edge buffer must be exactly 2 distinct face letters, "
                f"got: {self.edge_buffer!r}"
            )

        current_transition = color_transition_dict[self.orientation]

        transitioned_colors = []
        for letter in self.edge_buffer:
            color_enum = to_color(letter)
            if color_enum is None:
                raise ValueError(f"Invalid face character in edge buffer: {letter}")
            transitioned_colors.append(current_transition[color_enum])

        transitioned_edge_buffer = tuple(transitioned_colors)

        for edge in solved_edges:
            if set(edge[0]) == set(transitioned_edge_buffer):
                if transitioned_edge_buffer[0] == edge[0][0]:
                    self.edge_buffer_position = edge[1]
                else:
                    self.edge_buffer_position = (edge[1][1], edge[1][0])
                return

        raise ValueError(
            f"{self.edge_buffer!r} is not a valid edge (the two faces must be adjacent)."
        )
