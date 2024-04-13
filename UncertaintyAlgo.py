import copy
from typing import Tuple

from ValueIteretion import ValueIteration
from Graph import Graph
from name_tuppels import Edge


class UncertaintyAlgo:
    def __init__(self, graph: Graph):
        self.graph = graph

    def start_algo(self) -> {Tuple[Edge]: [[int]]}:
        believe_state = None
        value_iteration_algo = ValueIteration(believe_state, copy.deepcopy(self.graph))
        return value_iteration_algo.run_algo()

