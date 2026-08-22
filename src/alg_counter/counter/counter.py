"""
Module containing the core simulation logic for counting algorithms.

The `Counter` class simulates the process of solving a Rubik's Cube
blindfolded (3bld), tracking the number of targets, twists, flips,
cycle breaks, and parity to calculate the exact number of algorithms used.
"""

from math import ceil
from typing import cast

from alg_counter.model.cube import Cube
from alg_counter.state.state import State


class Counter:
    """Core engine that simulates a blindfolded solve to count algorithms.

    Attributes:
        state (State): The configuration state containing buffers and parity flags.
        cube (Cube): The physical cube model containing current colors.
        corners_dict (dict[tuple[int, int, int], tuple[int, int, int]]): A mapping of
            solved corner positions to their current scrambled positions.
        edges_dict (dict[tuple[int, int], tuple[int, int]]): A mapping of
            solved edge positions to their current scrambled positions.
    """

    state: State
    cube: Cube
    corners_dict: dict[tuple[int, int, int], tuple[int, int, int]]
    edges_dict: dict[tuple[int, int], tuple[int, int]]

    def __init__(self, cube: Cube, state: State):
        """Initializes the Counter and extracts the initial corner states.

        Args:
            cube (Cube): The scrambled cube to be analyzed.
            state (State): The solving state (buffers, orientation).
        """
        self.state = state
        self.cube = cube
        self.corners_dict = cube.get_current_corners()
        self.edges_dict = {}
        self.extend_corners_dict()

    def count(self) -> int:
        """Runs the full simulation and calculates the total algorithms needed.

        Returns:
            int: The total number of algorithms executed (corners + edges + parity).
        """
        return self.simulate_corners() + self.simulate_edges() + int(self.state.parity)

    def simulate_corners(self) -> int:
        """Simulates the corner execution phase.

        Tracks targets, unoriented but solved corners (twists), and handles
        cycle breaks. Also determines if edge execution will require parity adjustment.

        Returns:
            int: The number of algorithms required to solve the corners.
        """
        targets = 0
        corners_twisted = 0.0
        num_of_twists = 0.0
        solved = 0.0

        for key, val in self.corners_dict.copy().items():
            if set(key) == set(val):
                if set(key) == set(self.state.corner_buffer_position):
                    continue
                self.corners_dict.pop(key)

                if key == (val[1:] + val[:1]):
                    corners_twisted += 1 / 3
                    num_of_twists += 1 / 3
                elif key == (val[2:] + val[:2]):
                    corners_twisted += 1 / 3
                    num_of_twists += 2 / 3
                solved += 1 / 3

        target = self.corners_dict[self.state.corner_buffer_position]
        self.remove_element(self.state.corner_buffer_position)

        # Total corners minus buffer = 7
        while round(solved) < 7:
            if set(target) == set(self.state.corner_buffer_position):
                target_broken_into = next(iter(self.corners_dict.keys()))
                new_target = self.corners_dict[target_broken_into]
                self.change_element(target_broken_into, target)
                target = new_target
            else:
                new_target = self.corners_dict[target]
                solved += 1
                self.remove_element(target)
                target = new_target
            targets += 1

        if targets % 2 == 1:
            self.state.parity = True

        return targets // 2 + ceil(
            (corners_twisted + (0 if num_of_twists % 3 == 0 else 1)) / 2
        )

    def simulate_edges(self) -> int:
        """Simulates the edge execution phase.

        Adjusts the cube state for parity if necessary, tracks targets,
        unoriented edges (flips), and handles cycle breaks.

        Returns:
            int: The number of algorithms required to solve the edges.
        """
        targets = 0
        edges_flipped = 0.0
        solved = 0.0

        if self.state.parity:
            self.cube.adjust_for_parity()

        self.edges_dict = self.cube.get_current_edges()
        self.extend_edges_dict()

        for key, val in self.edges_dict.copy().items():
            if set(key) == set(val):
                if set(key) == set(self.state.edge_buffer_position):
                    continue
                self.edges_dict.pop(key)

                if key[0] == val[1]:
                    edges_flipped += 1 / 2
                solved += 1 / 2

        target = self.edges_dict[self.state.edge_buffer_position]
        self.remove_element(self.state.edge_buffer_position)

        # Total edges minus buffer = 11
        while solved < 11:
            if set(target) == set(self.state.edge_buffer_position):
                target_broken_into = next(iter(self.edges_dict.keys()))
                new_target = self.edges_dict[target_broken_into]
                self.change_element(target_broken_into, target)
                target = new_target
            else:
                new_target = self.edges_dict[target]
                solved += 1
                self.remove_element(target)
                target = new_target
            targets += 1

        return targets // 2 + ceil(edges_flipped / 2)

    def extend_corners_dict(self) -> None:
        """Populates the corners dictionary with all 3 possible orientations for each piece."""
        for element in list(self.corners_dict.keys()):
            value = self.corners_dict[element]
            # Jawne indeksowanie zamiast wycinków (slicing)
            self.corners_dict[(element[1], element[2], element[0])] = (
                value[1],
                value[2],
                value[0],
            )
            self.corners_dict[(element[2], element[0], element[1])] = (
                value[2],
                value[0],
                value[1],
            )

    def extend_edges_dict(self) -> None:
        """Populates the edges dictionary with both possible orientations for each piece."""
        for element in list(self.edges_dict.keys()):
            value = self.edges_dict[element]
            self.edges_dict[(element[1], element[0])] = (value[1], value[0])

    def remove_element(self, coords: tuple[int, int, int] | tuple[int, int]) -> None:
        """Removes a solved piece (and all its orientations) from the tracking dictionary.

        Args:
            coords (tuple[int, int, int] | tuple[int, int]): The indices of the piece to remove.
        """
        if len(coords) == 2:
            # Ręczne "rzutowanie" typu, żeby upewnić MyPy
            c2 = cast(tuple[int, int], coords)
            self.edges_dict.pop(c2)
            self.edges_dict.pop((c2[1], c2[0]))
        elif len(coords) == 3:
            c3 = cast(tuple[int, int, int], coords)
            self.corners_dict.pop(c3)
            self.corners_dict.pop((c3[1], c3[2], c3[0]))
            self.corners_dict.pop((c3[2], c3[0], c3[1]))

    def change_element(
        self,
        coords_key: tuple[int, int, int] | tuple[int, int],
        coords_new: tuple[int, int, int] | tuple[int, int],
    ) -> None:
        """Updates the target position of a piece and all its rotational equivalents.

        Args:
            coords_key (tuple[int, int, int] | tuple[int, int]): The current position key.
            coords_new (tuple[int, int, int] | tuple[int, int]): The new target position.
        """
        if len(coords_key) == 2:
            k2 = cast(tuple[int, int], coords_key)
            v2 = cast(tuple[int, int], coords_new)
            self.edges_dict[k2] = v2
            self.edges_dict[(k2[1], k2[0])] = (v2[1], v2[0])
        elif len(coords_key) == 3:
            k3 = cast(tuple[int, int, int], coords_key)
            v3 = cast(tuple[int, int, int], coords_new)
            self.corners_dict[k3] = v3
            self.corners_dict[(k3[1], k3[2], k3[0])] = (v3[1], v3[2], v3[0])
            self.corners_dict[(k3[2], k3[0], k3[1])] = (v3[2], v3[0], v3[1])
