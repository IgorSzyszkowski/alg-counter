from alg_counter.counter.counter import Counter
from alg_counter.model.cube import Cube
from alg_counter.scrambler.scramble import Scramble
from alg_counter.state.state import State

to_letters_dict = {
    (0, 36, 47) : "A",
    (36, 47, 0) : "D",
    (47, 0, 36) : "O",
    (2, 45, 11) : "B",
    (45, 11, 2) : "N",
    (11, 2, 45) : "K",
    (6, 18, 38) : "C",
    (18, 38, 6) : "H",
    (38, 6, 18) : "E",
    (24, 27, 44) : "J",
    (27, 44, 24) : "S",
    (44, 24, 27) : "F",
    (26, 15, 29) : "I",
    (15, 29, 26) : "M",
    (29, 26, 15) : "T",
    (42, 33, 53) : "G",
    (33, 53, 42) : "W",
    (53, 42, 33) : "P",
    (17, 51, 35) : "L",
    (51, 35, 17) : "R",
    (35, 17, 51) : "U",
    (1, 46) : "A",
    (46, 1) : "O",
    (5, 10) : "B",
    (10, 5) : "K",
    (3, 37) : "C",
    (37, 3) : "D",
    (21, 41) : "J",
    (41, 21) : "E",
    (23, 12) : "H",
    (12, 23) : "N",
    (39, 50) : "G",
    (50, 39) : "P",
    (14, 48) : "L",
    (48, 14) : "S",
    (25, 28) : "I",
    (28, 25) : "T",
    (16, 32) : "M",
    (32, 16) : "U",
    (43, 30) : "F", 
    (30, 43) : "Z",
    (52, 34) : "R",
    (34, 52) : "W",
    (20, 8, 9) : "X",
    (8, 9, 20) : "X",
    (9, 20, 8) : "X",
    (7, 19) : "X",
    (19, 7) : "X",
}

def count_algorithms(
    scr: str,
    corner_buffer: str = "UFR",
    edge_buffer: str = "UF",
    orientation: tuple[str, str] = ("W", "G"),
) -> int:
    cube = Cube()
    scramble = Scramble(scr)
    scramble.scramble_cube(cube)
    state = State(
        orientation=orientation,
        corner_buffer=corner_buffer,
        edge_buffer=edge_buffer,
    )
    counter = Counter(cube, state)
    return counter.count()

def get_path(
    scr: str,
    corner_buffer: str = "UFR",
    edge_buffer: str = "UF",
    orientation: tuple[str, str] = ("W", "G"),
) -> list[str]:
    cube = Cube()
    scramble = Scramble(scr)
    scramble.scramble_cube(cube)
    state = State(
        orientation=orientation,
        corner_buffer=corner_buffer,
        edge_buffer=edge_buffer,
    )
    counter = Counter(cube, state)
    counter.count()
    return translate_path(counter.corner_targets), translate_path(counter.edge_targets)

def translate_path(path: tuple[int, int, int] | tuple[int, int, int]) -> list[str]:
    result_list = [f"{to_letters_dict[path[2 * i]]}{to_letters_dict[path[2 * i + 1]]}" for i in range(len(path) // 2)]
    if len(path) % 2 == 1:
        result_list.append(to_letters_dict[path[len(path) - 1]])
    return result_list

def add_opposite(pairs: list[str]) -> None:
    return [pairs.append(pair[1] + pair[0]) for pair in pairs.copy()]

if __name__ == "__main__":
    wanted_corners = ["EN", "EU", "IJ", "IW", "SW", "UW"] #EN EU
    add_opposite(wanted_corners)
    wanted_edges = []
    add_opposite(wanted_edges)
    for i in range(30):
        while True:
            scramble = Scramble.get_wca_scramble()
            n_algs = count_algorithms(scramble)
            corner_path, edge_path = get_path(scramble)

            # Zliczamy, ile elementów z listy `wanted_corners` występuje w `corner_path`
            matching_corners = sum(1 for pair in corner_path if pair in wanted_corners)
            matching_edges = sum(1 for pair in edge_path if pair in wanted_edges)

            # Warunki akceptacji scramble'a:
            # 1. Co najmniej 2 elementy z `wanted_corners` muszą znajdować się w `corner_path`
            if wanted_corners and matching_corners < 2:
                continue
                
            # 2. Jeśli zdefiniowano `wanted_edges`, w `edge_path` musi znaleźć się co najmniej 1
            if wanted_edges and matching_edges < 1:
                continue
                
            # 3. Liczba algorytmów w przedziale (0, 8]
            if 0 < n_algs <= 8:
                break

        print(f"{i}:", scramble)