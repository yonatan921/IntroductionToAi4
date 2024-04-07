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

    def generate_edge_subsets(self) -> [[Edge]]:
        subsets = []

        def generate_subsets(index, current_subset):
            if index == len(self.graph.fragile):
                subsets.append(current_subset[:])  # Append a copy of the current subset
                return

            # Include the edge with original probability
            generate_subsets(index + 1, current_subset + [self.graph.fragile[index]])

            # Include the edge with probability 0
            generate_subsets(index + 1,
                             current_subset + [Edge(v1=self.graph.fragile[index].v1, v2=self.graph.fragile[index].v2, prob=0)])

            # Include the edge with probability 1
            generate_subsets(index + 1,
                             current_subset + [Edge(v1=self.graph.fragile[index].v1, v2=self.graph.fragile[index].v2, prob=1)])

        generate_subsets(0, [])  # Start with index 0 and empty subset
        return subsets
