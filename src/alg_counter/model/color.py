from enum import Enum, auto


class Color(Enum):
    U = auto()
    D = auto()
    L = auto()
    R = auto()
    B = auto()
    F = auto()

def to_color(color: str) -> Color | None:
    match color:
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