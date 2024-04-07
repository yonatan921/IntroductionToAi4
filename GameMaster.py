from typing import Tuple

from Graph import Graph
from Problem import Problem
from UncertaintyAlgo import UncertaintyAlgo
from name_tuppels import Edge


class GameMaster:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.update_packages()
        self.graph.aigent.problem = Problem(self.graph, lambda g: g.game_over())
        self.graph.aigent.algo = UncertaintyAlgo(graph)

    def start_game(self):
        while not self.game_over():
            print(self)
            # self.graph.explore_edges()
            self.graph.generate_states()
            self.graph.aigent.make_move(self.graph)
            self.graph.timer += 1

        print(self)

    def game_over(self):
        return self.graph.game_over()

    def update_packages(self):
        self.update_graph_packages()
        self.update_aigent_packages()

    def update_aigent_packages(self):
        self.graph.aigent.update_packages(self.graph.timer)

    def update_graph_packages(self):
        self.graph.update_packages()

    def __str__(self):
        return str(self.graph)
