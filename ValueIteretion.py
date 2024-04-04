import copy
from collections import deque

import numpy as np

from Graph import Graph
from name_tuppels import Edge, Point
import math


class ValueIteration:
    def __init__(self, believe_state: [Edge], graph: Graph):
        self.believe_state = believe_state
        self.graph = graph
        self.graph.create_prob_edges(believe_state)

    def run_algo(self) -> np.ndarray:
        target: Point = list(self.graph.aigent.pakages)[0].point_dst
        if not self.check_connectivity(self.graph.aigent.point, target):
            return None
        old_grid: np.ndarray = self.create_grid()
        new_grid: np.ndarray = np.copy(old_grid)
        while True:
            for row in range(len(new_grid)):
                for col in range(len(new_grid[0])):
                    current_point = Point(col, row)
                    if current_point == target:
                        continue
                    total = []
                    for point in self.graph.available_moves(current_point):
                        not_broken = self.graph.edge_cost(current_point, point) * (-1 + new_grid[point.y][point.x])
                        broken = (1 - self.graph.edge_cost(current_point, point)) * (
                                -1 + new_grid[current_point.y][current_point.x])
                        total.append(not_broken + broken)
                    if total:
                        new_grid[row][col] = max(total)

            if np.all(old_grid == new_grid):
                break

            old_grid = np.copy(new_grid)

        return new_grid

    def create_grid(self) -> np.ndarray:
        # Initialize grid with zeros
        grid = np.zeros((len(self.graph.grid), len(self.graph.grid[0])))
        # Set the target point to 0
        target: Point = list(self.graph.aigent.pakages)[0].point_dst
        grid[target.y][target.x] = 0
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
