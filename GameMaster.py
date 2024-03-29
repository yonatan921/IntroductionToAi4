from Graph import Graph
from Problem import Problem


class GameMaster:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.update_packages()
        self.graph.agents[0].problem = Problem(self.graph, lambda g: g.game_over())

    def start_game(self):
        while not self.game_over():
            print(self)
            self.graph.timer += 1
            for aigent in self.graph.agents:
                self.update_packages()
                self.graph.turn += 1
        print(self)

    def game_over(self):
        return self.graph.game_over()

    def update_packages(self):
        self.update_graph_packages()
        self.update_aigent_packages()

    def update_aigent_packages(self):
        for aigent in self.graph.agents:
            aigent.update_packages(self.graph.timer)

    def update_graph_packages(self):
        self.graph.update_packages()

    def __str__(self):
        return str(self.graph)
