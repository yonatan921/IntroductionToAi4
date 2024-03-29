import abc
from Node import Node
from ReturnStatus import ReturnStatus
from Tile import Tile
from name_tuppels import Point, Edge


class Aigent(abc.ABC, Tile):
    def __init__(self, starting_point: Point, _id):
        super().__init__(starting_point)
        self.id = _id
        self.score = 0
        self.pakages = set()

    @abc.abstractmethod
    def make_move(self, graph):
        """
        Consider fragile.
        Consider update packages.


        :return:
        """
        pass

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
    def __init__(self, starting_point: Point, _id, fragile_edges: {Edge}):
        super().__init__(starting_point, _id)
        self.symbol = f"AI{_id} "
        self.moves = []
        self.problem = None
        self.algo = None
        self.fragile_edges: {Edge} = fragile_edges

    def make_move(self, graph):
        if self.moves is None:
            self.move_agent(graph, self.point)

        new_location = self.moves.pop().action
        self.move_agent(graph, new_location)
        if not self.moves:
            self.run_algo()

    def parse_move(self, node: Node, return_status):
        if return_status == ReturnStatus.Fail:
            self.moves = None
        elif return_status == ReturnStatus.Cutoff:
            while node:
                self.moves.append(node)
                node = node.parent
            self.moves.pop()
            self.moves = [self.moves.pop()]
        else:
            while node:
                self.moves.append(node)
                node = node.parent
            self.moves.pop()

    def run_algo(self):
        last_node, return_status = self.algo(self.problem)
        self.algo.expands_nums = 0
        self.parse_move(last_node, return_status)

    def exist_edge(self, edge: Edge):
        self.fragile_edges.pop(edge)
        exist_edge = Edge(edge.v1, edge.v2, 0)
        self.fragile_edges.add(exist_edge)

    def dose_not_exist_edge(self, edge: Edge):
        self.fragile_edges.pop(edge)
        exist_edge = Edge(edge.v1, edge.v2, 1)
        self.fragile_edges.add(exist_edge)
