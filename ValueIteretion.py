from collections import deque
from typing import Optional

import numpy as np

from Graph import Graph
from name_tuppels import Edge, Point
import copy


class ValueIteration:
    def __init__(self, believe_state: [Edge], graph: Graph):
        self.believe_state = believe_state
        self.graph = graph

    def run_algo(self) -> Optional[np.ndarray]:
        target: Point = list(self.graph.aigent.pakages)[0].point_dst
        if not self.check_connectivity(self.graph.aigent.point, target):
            return None
        old_grid: np.ndarray = self.create_grid()
        states = self.get_all_states()
        for state in states:
            if 'U' in state:
                continue
            new_graph = copy.deepcopy(self.graph)
            i = 0
            while i < len(state):
                actual_state = state[i]
                if actual_state == 'T':
                    new_graph.remove_edge(self.graph.fragile[i])
                    new_graph.fragile.remove(self.graph.fragile[i])
                i += 1
            while not self.visited_all(state, new_graph):
                for row in range(len(old_grid)):
                    for col in range(len(old_grid[0])):
                        current_point = Point(col, row)
                        total = []
                        current_point_state = tuple((current_point,))
                        for actual_state in state:
                            current_point_state += (actual_state,)
                        for point in new_graph.available_moves(current_point):
                            point_state = tuple((point,))
                            for actual_state in state:
                                point_state += (actual_state,)
                            policy = -1 + self.graph.states[point_state]
                            if policy > self.graph.states[current_point_state]:
                                total.append(policy)
                        if total:
                            self.graph.states[current_point_state] = max(total)

        for state in self.graph.states:
            for i, s in enumerate(state):
                if s == 'U':
                    temp_true = state[:i] + ('T',) + state[i + 1:]
                    temp_false = state[:i] + ('F',) + state[i + 1:]
                    fragile_edge = self.graph.fragile[i - 1]
                    policy = (fragile_edge[-1] * self.graph.states[temp_true]) + (
                            (1 - fragile_edge[-1]) * self.graph.states[temp_false])
                    self.graph.states[state] = policy

        return self.graph.states

    def visited_all(self, state, new_graph):
        for actual_state in self.graph.states:
            unknown_state = actual_state[1:]
            if state == unknown_state and self.graph.states[actual_state] == -np.inf and len(
                    new_graph.available_moves(actual_state[0])) > 0:
                return False
        return True

    def get_all_states(self):
        states = set()
        for state in self.graph.states:
            edge_states = state[1:]
            states.add(edge_states)
        return states

    def create_grid(self) -> np.ndarray:
        # Initialize grid with -inf
        grid = np.full((len(self.graph.grid), len(self.graph.grid[0])), -np.inf)
        # Set the target point to 0
        target_point = list(self.graph.aigent.pakages)[0].point_dst
        grid[target_point.y][target_point.x] = 0
        return grid

    def check_connectivity(self, start: Point, end: Point):
        visited = set()
        queue = deque([start])

        while queue:
            current_vertex = queue.popleft()
            if current_vertex == end:
                return True
            visited.add(current_vertex)
            for neighbor in self.graph.edges.get(current_vertex):
                if neighbor not in visited:
                    queue.append(neighbor)

        return False
