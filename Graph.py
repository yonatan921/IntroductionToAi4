import random
from itertools import product

import numpy as np

from Aigent import AiAigent
from Tile import Tile, Package
from name_tuppels import Point, Edge


class Graph:
    def __init__(self, max_x: int, max_y: int, blocks: {Edge}, fragile: {frozenset}, agents: [AiAigent], timer,
                 packages):
        self.grid = None
        self.edges = None
        self.relevant_packages = set()
        self.fragile = fragile
        self.aigent: AiAigent = agents
        self.blocks = blocks
        self.init_grid(max_x, max_y, blocks)
        self.timer = timer
        self.all_packages = packages
        self.turn = 0
        self.states = {}
        self.all_states = None

    def init_grid(self, max_x, max_y, blocks: {frozenset}):
        self.grid = [[Tile(Point(i, j)) for i in range(max_x + 1)] for j in range(max_y + 1)]

        self.add_aigent(self.aigent)
        self.edges = self.create_neighbor_dict()
        for edge in blocks:
            self.remove_edge(edge)

    def game_over(self):
        return len(self.relevant_packages) == 0 and self.aigent.game_over()

    def add_aigent(self, aigent: AiAigent):
        self.grid[aigent.point.y][aigent.point.x] = aigent

    def add_package(self, package: Package):
        if package.point == self.aigent.point:
            self.aigent.pakages.add(package)
            package.picked_up = True
            self.all_packages.remove(package)
            if package.point_dst == self.aigent.point:
                self.aigent.pakages.remove(package)
                self.aigent.score += 1
            return
        self.grid[package.point.y][package.point.x] = package

    def update_packages(self):
        self.relevant_packages = {package for package in self.all_packages if
                                  package.from_time <= self.timer <= package.dead_line and not package.picked_up}
        for package in self.relevant_packages:
            self.add_package(package)

        self.relevant_packages = {package for package in self.all_packages if
                                  package.from_time <= self.timer <= package.dead_line and not package.picked_up}

        goal: Point = list(self.aigent.pakages)[0].point_dst
        goal_tile = self.grid[goal.y][goal.x]
        goal_tile.symbol = "G"



    def can_move(self, location: Point, new_location: Point):
        if location == new_location:
            return True
        return self.edges[location].get(new_location) is not None and self.aigent.point != new_location

    def get_packages_to_take(self):
        return {package.point for package in self.relevant_packages}

    def get_packages_to_deliver(self):
        return {package.point_dst for package in self.relevant_packages}

    def __str__(self):
        aigents_string = str(self.aigent.string_state()) + "\n"
        matrix_string = "\n".join(" ".join(str(tile) for tile in row) for row in self.grid)
        return aigents_string + matrix_string + '\n'

    def remove_edge(self, edge: {Point}):
        p1, p2 = edge.v1, edge.v2
        if p1 in self.edges and len(self.edges[p1]) > 0:
            for point in self.edges[p1]:
                if p2 == point:
                    del self.edges[p1][p2]
                    break
        if p2 in self.edges and len(self.edges[p2]) > 0:
            for point in self.edges[p2]:
                if p1 == point:
                    del self.edges[p2][p1]
                    break

    def create_neighbor_dict(self):
        num_rows, num_cols = len(self.grid), len(self.grid[0])

        neighbor_dict = {
            Point(j, i): {
                Point(j, i - 1): 1 if i > 0 else None,
                Point(j, i + 1): 1 if i < num_rows - 1 else None,
                Point(j - 1, i): 1 if j > 0 else None,
                Point(j + 1, i): 1 if j < num_cols - 1 else None
            }
            for i in range(num_rows)
            for j in range(num_cols)
        }
        neighbor_dict = {coord: {k: v for k, v in neighbors.items() if v is not None} for coord, neighbors in
                         neighbor_dict.items()}

        return neighbor_dict

    def remove_tile(self, point: Point):
        # remove agent
        self.grid[point.y][point.x] = Tile(point)

    def move_agent(self, org_point: Point, new_point: Point):
        # Add agent to new place
        get_agent = self.grid[org_point.y][org_point.x]
        self.grid[new_point.y][new_point.x] = get_agent

        # remove agent
        self.remove_tile(org_point)

    def available_moves(self, my_point: Point) -> [Point]:
        return [point for point, _ in self.edges[my_point].items()]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False
        return self.__key() == other.__key()

    def __key(self):
        return tuple(self.relevant_packages), tuple(self.fragile), self.aigent

    def explore_edges(self):
        for edge in self.fragile:
            if self.aigent.point in [edge.v1, edge.v2]:

                random_number = random.random()
                if random_number <= edge.prob:
                    self.remove_edge(edge)
                    self.fragile.remove(edge)

    def generate_states(self):
        self.states = {}
        vertices = set()

        # Collect all vertices from edges and their neighbors
        for edge, neighbors in self.edges.items():
            vertices.add(edge)
            vertices.update(neighbors.keys())

        # Generate states for each vertex
        for vertex in vertices:
            # Generate all possible combinations of edge states
            edge_states = product(*[['T', 'F', 'U'] for _ in range(len(self.fragile))])
            # Create states for each combination
            for edge_state in edge_states:
                # Create the key as a tuple of vertex and edge states
                state_key = (vertex,) + edge_state
                # Assign the value as -np.inf
                self.states[state_key] = -np.inf
            for edge_state in self.states:
                if edge_state[0] == list(self.aigent.pakages)[0].point_dst:
                    self.states[edge_state] = 0
