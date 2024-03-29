from GameMaster import GameMaster
from Graph import Graph
from Parser import Parser


def main():
    parser = Parser()
    graph = Graph(parser.max_x, parser.max_y, parser.blocks, parser.fragile, parser.aigent, 0, parser.packages)
    game_master = GameMaster(graph)


if __name__ == '__main__':
    main()
