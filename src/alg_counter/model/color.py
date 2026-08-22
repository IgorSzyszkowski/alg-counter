"""
Module defining the colors/faces of a Rubik's Cube.
"""

from enum import Enum, auto


class Color(Enum):
    """Represents the six standard faces (colors) of a Rubik's Cube."""

    U = auto()  # Up
    D = auto()  # Down
    L = auto()  # Left
    R = auto()  # Right
    B = auto()  # Back
    F = auto()  # Front


def to_color(color: str) -> Color | None:
    """Converts a string representation of a face to a Color enum.

    Args:
        color (str): A string representing a face (e.g., "U", "R").

    Returns:
        Color | None: The corresponding Color enum member, or None if the string
            does not match any valid face.
    """
    match color.upper():
        case "U":
            return Color.U
        case "R":
            return Color.R
        case "L":
            return Color.L
        case "D":
            return Color.D
        case "F":
            return Color.F
        case "B":
            return Color.B
        case _:
            return None
