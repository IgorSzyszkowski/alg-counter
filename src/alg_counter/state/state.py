"""
Module defining the simulation state, including buffers, parity, and cube orientation.
"""

from alg_counter.model.color import Color, to_color
from alg_counter.model.cube import solved_corners, solved_edges

# Maps a starting orientation (Top color, Front color) to a dictionary
# that translates logical standard faces to the newly oriented physical faces.
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
    """State of the cube containing important information during the solving simulation.

    Tracks the chosen buffers, the cube's orientation, parity status,
    and translates logical buffer strings into their physical string indices.

    Attributes:
        corner_buffer (str): The logical representation of the corner buffer (e.g., "UFR").
        edge_buffer (str): The logical representation of the edge buffer (e.g., "UF").
        orientation (tuple[str, str]): The orientation of the cube as (Top, Front) colors (e.g., ("W", "G")).
        parity (bool): Flag indicating if the cube state currently has parity (odd number of targets).
        corner_buffer_position (tuple[int, int, int]): The physical indices of the corner buffer on the cube string.
        edge_buffer_position (tuple[int, int]): The physical indices of the edge buffer on the cube string.
    """

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
            orientation (tuple[str, str], optional): The starting orientation (Top, Front). Defaults to ("W", "G").
            corner_buffer (str, optional): The logical corner buffer position. Defaults to "UFR".
            edge_buffer (str, optional): The logical edge buffer position. Defaults to "UF".
        """
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
            ValueError: If the `corner_buffer` string contains an invalid face character.
        """
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
                break

    def get_edge_buffer_position(self) -> None:
        """Calculates the physical string indices for the chosen edge buffer.

        Translates the logical edge buffer (e.g., "UF") into physical indices
        based on the current cube orientation and stores it in `self.edge_buffer_position`.

        Raises:
            ValueError: If the `edge_buffer` string contains an invalid face character.
        """
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
                break
