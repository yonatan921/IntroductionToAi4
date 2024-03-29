import copy
from typing import Callable

from Graph import Graph


class Problem:
    def __init__(self, init_state: Graph, goal_state: Callable[[Graph], bool]):
        self.init_state = init_state
        self.goal_state = goal_state

    @staticmethod
    def find_successors(graph):
        successors = {}
        for available_point in graph.available_moves(graph.agents[graph.turn % 2].point):
            new_graph = copy.deepcopy(graph)
            new_graph.turn += 1
            new_graph.update_packages()
            new_graph.timer += graph.turn % 2
            new_graph.agents[graph.turn % 2].move_agent(new_graph, available_point)
            successors[available_point] = new_graph

        return successors
