from alg_counter.state.state import State
from alg_counter.model.cube import Cube
from math import ceil

class Counter:
    state: State
    cube: Cube
    corners_dict: dict[tuple[int, int, int], tuple[int, int, int]]
    edges_dict: dict[tuple[int, int], tuple[int, int]]

    def __init__(self, cube: Cube, state: State):
        self.state = state
        self.cube = cube
        self.corners_dict = cube.get_current_corners()
        self.edges_dict = None
        self.extend_corners_dict()
        
    def count(self) -> int:
        return self.simulate_corners() + self.simulate_edges() + int(self.state.parity)

    def simulate_corners(self) -> int:
        targets = 0
        corners_twisted = 0
        num_of_twists = 0
        solved = 0
        for key, val in self.corners_dict.copy().items():
            if set(key) == set(val):
                if set(key) == set(self.state.corner_buffer_position): 
                    continue
                self.corners_dict.pop(key)
                if key == (val[1:] + val[:1]):
                    corners_twisted += 1/3
                    num_of_twists += 1/3
                elif key == (val[2:] + val[:2]):
                    corners_twisted += 1/3
                    num_of_twists += 2/3
                solved += 1/3
        target = self.corners_dict[self.state.corner_buffer_position]
        self.remove_element(self.state.corner_buffer_position)
        while solved < 7:
            if set(target) == set(self.state.corner_buffer_position):
                target_broken_into = list(self.corners_dict.keys())[0]
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
        return targets // 2 + ceil((corners_twisted + (0 if num_of_twists % 3 == 0 else 1)) / 2)

    def simulate_edges(self) -> int:
        targets = 0
        edges_fliped = 0
        solved = 0
        if(self.state.parity):
            self.cube.adjust_for_parity()
        self.edges_dict = self.cube.get_current_edges()
        self.extend_edges_dict()
        for key, val in self.edges_dict.copy().items():
            if set(key) == set(val):
                if set(key) == set(self.state.edge_buffer_position): 
                    continue
                self.edges_dict.pop(key)
                if key[0] == val[1]:
                    edges_fliped += 1/2
                solved += 1/2
        target = self.edges_dict[self.state.edge_buffer_position]
        self.remove_element(self.state.edge_buffer_position)
        while solved < 11:
            if set(target) == set(self.state.edge_buffer_position):
                target_broken_into = list(self.edges_dict.keys())[0]
                new_target = self.edges_dict[target_broken_into]
                self.change_element(target_broken_into, target)
                target = new_target
            else:
                new_target = self.edges_dict[target]
                solved += 1
                self.remove_element(target)
                target = new_target
            targets += 1
        return targets // 2 + ceil(edges_fliped / 2)

    def extend_corners_dict(self) -> None:
        for element in self.corners_dict.copy().keys():
            value = self.corners_dict[element]
            self.corners_dict[element[1:] + element[:1]] = value[1:] + value[:1]
            self.corners_dict[element[2:] + element[:2]] = value[2:] + value[:2]

    def extend_edges_dict(self) -> None:
        for element in self.edges_dict.copy().keys():
            value = self.edges_dict[element]
            self.edges_dict[element[1:] + element[:1]] = value[1:] + value[:1]

    def remove_element(self, coords: tuple[int, int, int] | tuple[int, int]) -> None:
        if len(coords) == 2:
            self.edges_dict.pop(coords)
            self.edges_dict.pop(coords[1:] + coords[:1])
        elif len(coords) == 3:
            self.corners_dict.pop(coords)
            self.corners_dict.pop(coords[1:] + coords[:1])
            self.corners_dict.pop(coords[2:] + coords[:2])

    def change_element(self, coords_key: tuple[int, int, int] | tuple[int, int], coords_new: tuple[int, int, int] | tuple[int, int]) -> None:
        if len(coords_key) == 2:
            self.edges_dict[coords_key] = coords_new
            self.edges_dict[coords_key[1:] + coords_key[:1]] = coords_new[1:] + coords_new[:1]
        elif len(coords_key) == 3:
            self.corners_dict[coords_key] = coords_new
            self.corners_dict[coords_key[1:] + coords_key[:1]] = coords_new[1:] + coords_new[:1]
            self.corners_dict[coords_key[2:] + coords_key[:2]] = coords_new[2:] + coords_new[:2]