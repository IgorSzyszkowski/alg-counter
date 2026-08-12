from dataclasses import dataclass, field
from typing import Dict, Callable, ClassVar, final
from itertools import product
import kociemba


@dataclass
class Scramble:
    _cube: str = field(default="UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    goal: ClassVar[str] = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    def __post_init__(self):
        self.moves: Dict[str, Callable[[str], str]] = {
            "U": self._U, "D": self._D, "L": self._L,
            "R": self._R, "F": self._F, "B": self._B
        }

    @property
    def cube(self) -> str:
        return self._cube

    @cube.setter
    def cube(self, value: str):
        if len(value) != 54:
            self._cube = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        else:
            self._cube = value

    def _rotate_face(self, cube_str: str, start: int) -> str:
        chars = list(cube_str)
        face = chars[start: start + 9]
        chars[start: start + 9] = [
            face[6], face[3], face[0],
            face[7], face[4], face[1],
            face[8], face[5], face[2],
        ]
        return "".join(chars)

    def _U(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 0)
        c = list(cube_str)
        temp = c[18:21]
        c[18:21] = c[9:12]
        c[9:12] = c[45:48]
        c[45:48] = c[36:39]
        c[36:39] = temp
        return "".join(c)

    def _D(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 27)
        c = list(cube_str)
        temp = c[24:27]
        c[24:27] = c[42:45]
        c[42:45] = c[51:54]
        c[51:54] = c[15:18]
        c[15:18] = temp
        return "".join(c)

    def _L(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 36)
        c = list(cube_str)
        temp = [c[0], c[3], c[6]]
        c[0], c[3], c[6] = c[53], c[50], c[47]
        c[53], c[50], c[47] = c[27], c[30], c[33]
        c[27], c[30], c[33] = c[18], c[21], c[24]
        c[18], c[21], c[24] = temp[0], temp[1], temp[2]
        return "".join(c)

    def _R(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 9)
        c = list(cube_str)
        temp = [c[2], c[5], c[8]]
        c[2], c[5], c[8] = c[20], c[23], c[26]
        c[20], c[23], c[26] = c[29], c[32], c[35]
        c[29], c[32], c[35] = c[51], c[48], c[45]
        c[51], c[48], c[45] = temp[0], temp[1], temp[2]
        return "".join(c)

    def _F(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 18)
        c = list(cube_str)
        temp = [c[6], c[7], c[8]]
        c[6], c[7], c[8] = c[44], c[41], c[38]
        c[44], c[41], c[38] = c[29], c[28], c[27]
        c[29], c[28], c[27] = c[9], c[12], c[15]
        c[9], c[12], c[15] = temp[0], temp[1], temp[2]
        return "".join(c)

    def _B(self, cube_str: str) -> str:
        cube_str = self._rotate_face(cube_str, 45)
        c = list(cube_str)
        temp = [c[0], c[1], c[2]]
        c[0], c[1], c[2] = c[11], c[14], c[17]
        c[11], c[14], c[17] = c[35], c[34], c[33]
        c[35], c[34], c[33] = c[42], c[39], c[36]
        c[42], c[39], c[36] = temp[0], temp[1], temp[2]
        return "".join(c)

    def execute(self, moves_str: str, in_place: bool = False) -> str | None:
        current_state = self._cube
        for move in moves_str.split():
            base = move[0]
            if base in self.moves:
                if move == base:
                    current_state = self.moves[base](current_state)
                elif move.endswith("'"):
                    for _ in range(3):
                        current_state = self.moves[base](current_state)
                elif move.endswith("2"):
                    for _ in range(2):
                        current_state = self.moves[base](current_state)

        if in_place:
            self._cube = current_state
            return None
        return current_state

all_moves = ["R", "R'", "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2", "D", "D'", "D2", "U", "U'", "U2"]
#all_moves = ["R", "L", "F", "B", "D", "U"]

def find_solution(scramble: Scramble) -> str:
    comb = list(product(all_moves, all_moves, all_moves, all_moves)) + list(product(all_moves, all_moves, all_moves)) + list(product(all_moves, all_moves)) + all_moves + [""]
    final_solution = ""
    for i in range(6):
        print(i)
        sol = ""
        best = 0
        for x in comb:
            new_cube = scramble.execute(" ".join(x))
            result = sum(1 for a, b in zip(new_cube, scramble.goal) if a == b) / len(scramble.goal)
            if result > best:
                best = result
                sol = " ".join(x) + " "
        final_solution += sol
        scramble.execute(sol, in_place=True)

    print(final_solution)
    return ""

if __name__ == "__main__":
    scramble = Scramble()
    scramble.execute("D B2 R2 B2 R2 D2 F2 U' L2 B2 R2 U B' L' F L F' L B2 R' D' F'", in_place=True)
    solution = find_solution(scramble)
    print(solution)
