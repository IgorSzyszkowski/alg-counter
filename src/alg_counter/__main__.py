"""
Main entry point for the alg-counter CLI application.
"""

import argparse
import sys

from alg_counter.counter.counter import Counter
from alg_counter.model.cube import Cube
from alg_counter.scrambler.scramble import Scramble
from alg_counter.state.state import State

VALID_COLORS = ["W", "Y", "G", "B", "O", "R"]


def parse_arguments() -> argparse.Namespace:
    """Parses the command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the
            scramble, buffers, and orientation.
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
    arg_parser.add_argument(
        "--corner-buffer",
        "-c",
        type=str,
        default="UFR",
        help="Corner buffer piece, given as three distinct face letters (e.g. UFR).",
    )
    arg_parser.add_argument(
        "--edge-buffer",
        "-e",
        type=str,
        default="UF",
        help="Edge buffer piece, given as two distinct face letters (e.g. UF).",
    )
    arg_parser.add_argument(
        "--top",
        "-t",
        type=str,
        default="W",
        choices=VALID_COLORS,
        help="Sticker color on the top face for the starting orientation.",
    )
    arg_parser.add_argument(
        "--front",
        "-f",
        type=str,
        default="G",
        choices=VALID_COLORS,
        help="Sticker color on the front face for the starting orientation.",
    )
    return arg_parser.parse_args()


def count_algorithms(
    scr: str,
    corner_buffer: str = "UFR",
    edge_buffer: str = "UF",
    orientation: tuple[str, str] = ("W", "G"),
) -> int:
    """Calculates the number of algorithms required to solve a given scramble.

    Args:
        scr (str): The string representing the scramble sequence.
        corner_buffer (str, optional): Logical corner buffer (e.g. "UFR").
            Defaults to "UFR".
        edge_buffer (str, optional): Logical edge buffer (e.g. "UF").
            Defaults to "UF".
        orientation (tuple[str, str], optional): Starting orientation as
            (top color, front color). Defaults to ("W", "G").

    Returns:
        int: The total number of algorithms required (corners + edges + parity).

    Raises:
        ValueError: If the scramble, buffers, or orientation are invalid.
    """
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

    try:
        num_of_algs = count_algorithms(
            scramble,
            corner_buffer=args.corner_buffer,
            edge_buffer=args.edge_buffer,
            orientation=(args.top, args.front),
        )
    except ValueError as error:
        print(f"alg-counter: error: {error}", file=sys.stderr)
        sys.exit(1)

    print(scramble, "-", num_of_algs)


if __name__ == "__main__":
    main()
