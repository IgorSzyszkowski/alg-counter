from alg_counter.model.cube import Cube
from alg_counter.scrambler.scramble import Scramble
from alg_counter.state.state import State
from alg_counter.counter.counter import Counter

def count_algorithms(scr: str) -> int:
    cube = Cube()
    scramble = Scramble(scr)
    scramble.scramble_cube(cube)
    state = State()
    counter = Counter(cube, state)
    return counter.count()

def generate_algs(n: int) -> list[str]:
    scrambles = []
    for _ in range(n):
        scrambles.append(Scramble.get_wca_scramble())
    return scrambles

def main() -> None:
    print(generate_algs(5))