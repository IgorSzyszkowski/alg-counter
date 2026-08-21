from statistics import mean, median

from alg_counter.counter.counter import Counter
from alg_counter.model.cube import Cube
from alg_counter.scrambler.scramble import Scramble
from alg_counter.state.state import State


def count_algorithms(scr: str) -> int:
    cube = Cube()
    scramble = Scramble(scr)
    scramble.scramble_cube(cube)
    state = State()
    counter = Counter(cube, state)
    return counter.count()


def generate_algs(n: int) -> list[str]:
    return [Scramble.get_wca_scramble() for _ in range(n)]


def main() -> None:
    scrambles = generate_algs(10000000)
    counted_algorithms = []
    for i, scr in enumerate(scrambles):
        length = count_algorithms(scr)
        counted_algorithms.append(length)
        if length <= 6:
            print(f"{(i / 100000):.3f}%", length, scr)

    for i in (
        x
        for x in range(min(counted_algorithms), max(counted_algorithms) + 1)
        if counted_algorithms.count(x) != 0
    ):
        print(
            f"{i}: {counted_algorithms.count(i)} ({(round(counted_algorithms.count(i) / len(counted_algorithms), 8) * 100):.6f}%)"
        )

    print(f"median: {median(counted_algorithms)}")
    print(f"mean: {mean(counted_algorithms)}")


if __name__ == "__main__":
    main()
