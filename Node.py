import copy

from name_tuppels import Point


class Node:
    def __init__(self, parent, action, state, depth, path_cost: int,heuristic,  evaluation_func):
        self.parent: Node = parent
        self.action: Point = action
        self.state = state
        self.depth: int = depth
        self.path_cost: int = path_cost
        self.heuristic = heuristic
        self.evaluation = evaluation_func(self, heuristic)

    def step_cost(self, node):
        pass

    def __key(self):
        return self.state

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.__key() == other.__key()
        return False

    def __lt__(self, other):
        return self.evaluation < other.evaluation

    def find_successors(self):
        successors = {}
        for available_point in self.state.available_moves(self.state.agents[0].point):
            new_graph = copy.deepcopy(self.state)
            new_graph.timer += 1
            new_graph.update_packages()
            new_graph.agents[0].move_agent(new_graph, available_point)
            successors[available_point] = new_graph

        return successors
