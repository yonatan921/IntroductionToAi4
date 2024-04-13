import abc
import sys
from typing import Tuple
from Tile import Tile
from name_tuppels import Point, Edge


class Aigent(abc.ABC, Tile):
    def __init__(self, starting_point: Point, _id):
        super().__init__(starting_point)
        self.id = _id
        self.score = 0
        self.pakages = set()

    def update_packages(self, timer):
        self.pakages = {package for package in self.pakages if package.from_time <= timer <= package.dead_line}

    def game_over(self):
        return len(self.pakages) == 0

    def no_op(self):
        pass

    def move_agent(self, graph, new_location):
        current_point = self.point
        edge_crossed = frozenset({current_point, new_location})
        # pick package from new location
        taken_packages = set()
        for package in graph.relevant_packages:
            if package.point == new_location:
                taken_packages.add(package)
                self.pakages.add(package)
                package.picked_up = True
                graph.remove_tile(package.point)
        graph.relevant_packages -= taken_packages
        graph.all_packages -= taken_packages
        # deliver package
        if len(self.pakages) > 0:
            deliver_packages = set()
            for package in self.pakages:
                if package.point_dst == new_location:
                    deliver_packages.add(package)
                    graph.remove_tile(package.point_dst)
                    self.score += 1
            self.pakages -= deliver_packages

        # move the agent
        if self.point != new_location:
            self.point = new_location
            graph.move_agent(current_point, new_location)

    def __key(self):
        return self.point, self.symbol, tuple(self.pakages), self.score

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Aigent):
            return False

        return self.__key() == other.__key()

    def string_state(self):
        return f"{self.symbol}: packages:{[pakage.to_string() for pakage in self.pakages]}, score: {self.score}"


class AiAigent(Aigent):
    def __init__(self, starting_point: Point, _id, fragile_edges: [Edge]):
        super().__init__(starting_point, _id)
        self.symbol = f"A"
        self.moves = []
        self.algo = None
        self.fragile_edges: Tuple[Edge] = fragile_edges

    def make_move(self, graph):
        policy = self.algo.start_algo()
        if policy is None:
            print("This state is irregular")
            sys.exit(0)
        print(policy)
        self.print_policy(policy)
        new_location = self.parse_policy(policy, graph)
        print(f"Best move ({new_location.x},{new_location.y})")
        print("-"*20)
        self.move_agent(graph, new_location)

    def parse_policy(self, policies, graph) -> Point:
        unknown_policies = {}
        for state in policies:
            if all(s == 'U' for s in state[1:]):
                unknown_policies[state] = policies[state]
        best_point = None
        best_utility = float("-inf")
        for point in graph.available_moves(self.point):
            utility = None
            for state in unknown_policies:
                if state[0] == point:
                    utility = unknown_policies[state]
                    break
            if utility > best_utility:
                best_utility = utility
                best_point = point
        return best_point

    def print_policy(self, policy: {Tuple[Point, str], int}) -> None:
        uknown_policy = {t[0]: util for t, util in policy.items() if all(val == "U" for val in t[1:])}
        max_x = max(point.x for point in uknown_policy)
        max_y = max(point.y for point in uknown_policy)

        # Initialize an empty matrix with dimensions (max_y + 1) x (max_x + 1)
        matrix = [[0] * (max_x + 1) for _ in range(max_y + 1)]

        # Populate the matrix with values from the dictionary
        for point, value in uknown_policy.items():
            matrix[point.y][point.x] = value

        print("Utility matrix")
        # Print the matrix
        for row in matrix:
            print(row)
