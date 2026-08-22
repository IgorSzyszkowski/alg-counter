# alg-counter

CLI tool that counts how many algorithms (executions) are needed to solve a Rubik's Cube scramble **blindfolded (3BLD)**, based on a chosen buffer and cube orientation.

## About

In 3BLD, pieces aren't solved one by one — each algorithm (commutator) resolves two pieces at once relative to a fixed **buffer** piece (e.g. corner UFR, edge UF). Scramble difficulty for a blindfolded solve is therefore measured in *algorithms*, not moves. `alg-counter` replays this tracing process on a simulated cube and returns the exact algorithm count, accounting for twists, flips, cycle breaks, and parity.

## How it works

- The cube is modeled as a 54-character string; moves permute indices in that string.
- Starting from the buffer, the tool traces the permutation cycle: every 2 targets = 1 executed algorithm.
- If a cycle closes back into the buffer before all pieces are placed, a **cycle break** costs one extra target.
- Correctly placed but misoriented pieces (twisted corners / flipped edges) are counted separately and paired into extra algorithms.
- An odd number of corner targets sets **parity**, adding one algorithm and swapping the UF/UR edge buffer before edges are traced.

## Project structure

```
alg-counter/
├── src/
│   └── alg_counter/
│       ├── counter/counter.py   # Algorithm-counting simulation
│       ├── model/
│       │   ├── color.py         # Face/color enum
│       │   └── cube.py          # Cube model, moves, piece mapping
│       ├── scrambler/scramble.py
│       ├── state/state.py       # Buffers, orientation, parity
│       └── __main__.py          # CLI entry point
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) recommended (repo uses `uv.lock` and `uv_build`)
- Runtime dependency: `ruff`
- Dev dependencies (`uv` dependency group): `ruff`, `mypy`, `pytest`

## Installation

```bash
git clone <repository-url>
cd alg-counter
uv sync
uv run alg-counter --scramble "R U R' U'"
```

Or with pip:

```bash
pip install -e .
alg-counter --scramble "R U R' U'"
```

## Usage

```
usage: alg-counter <scramble>

options:
  -h, --help            show this help message and exit
  --scramble SCRAMBLE, -s SCRAMBLE
                        WCA scramble string used to shuffle the cube. (default: )
```

| Flag | Short | Description | Default |
|---|---|---|---|
| `--scramble` | `-s` | WCA-notation scramble, e.g. `"R U R' U' F2"` | `""` → random WCA scramble |

**Verified examples:**

```bash
$ alg-counter -s "R U R' U' R' F R2 U' R' U' R U R' F'"
R U R' U' R' F R2 U' R' U' R U R' F' - 2

$ alg-counter -s "U U U U"
U U U U - 0
```

## Move notation

Standard WCA layer moves: `U D L R F B`, each optionally suffixed with `'` (counter-clockwise) or `2` (double). Any other token (slice moves, rotations) is rejected as an invalid scramble.

## Development

```bash
uv run ruff check .
uv run mypy .
```

## Limitations

- The buffer (`UFR` / `UF`) and orientation (`W`/`G`) are hardcoded via the default `State()` — not yet exposed as CLI flags, even though `State` supports any buffer and all 24 orientations.
- An invalid scramble raises an unhandled `ValueError` instead of a clean CLI error message.

## License

See [`LICENSE`](./LICENSE).

## Author

Igor Szyszkowski — i.szyszkowski06@gmail.com