"""
Main entry point for the alg-counter CLI application.
"""

import argparse

from alg_counter.counter.counter import Counter
from alg_counter.model.cube import Cube
from alg_counter.scrambler.scramble import Scramble
from alg_counter.state.state import State


def parse_arguments() -> argparse.Namespace:
    """Parses the command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the scramble.
    """
    arg_parser = argparse.ArgumentParser(
        prog="alg-counter",
        usage="alg-counter <scramble>",
        description="A tool for counting the number of algorithms needed to solve a Rubik's Cube blindfolded.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "--scramble",
        "-s",
        type=str,
        default="",
        help="The valid WCA scramble string used to shuffle the cube.",
    )
    return arg_parser.parse_args()


def count_algorithms(scr: str) -> int:
    """Calculates the number of algorithms required to solve a given scramble.

    Args:
        scr (str): The string representing the scramble sequence.

    Returns:
        int: The total number of algorithms required (corners + edges + parity).
    """
    cube = Cube()
    scramble = Scramble(scr)
    scramble.scramble_cube(cube)
    state = State()
    counter = Counter(cube, state)
    return counter.count()


def generate_alg() -> str:
    """Generates a random WCA-compliant scramble.

    Returns:
        str: Generated scramble.
    """
    return Scramble.get_wca_scramble()


def main() -> None:
    """Main execution block for the CLI program."""
    args = parse_arguments()
    scramble = generate_alg() if args.scramble == "" else args.scramble
    num_of_algs = count_algorithms(scramble)
    print(scramble, "-", num_of_algs)


if __name__ == "__main__":
    main()
