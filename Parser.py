import argparse

from Aigent import AiAigent
from Tile import Package
from name_tuppels import Point, Edge


class Parser:

    def __init__(self):

        parser = argparse.ArgumentParser(description="The Canadian Traveler Problem ")
        # Adding the 'filename' and 'algo' arguments
        parser.add_argument('--file', dest='filename', help="Input file path for the program")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Access the values using args.filename and args.algo
        filename = args.filename

        self.max_x = None
        self.max_y = None
        self.blocks: {Edge} = set()
        self.fragile: [Edge] = []
        self.packages: {Package} = set()
        self.aigent = None
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            words = line.split()
            if words and words[0][0] == "#":
                if self.command_word(words) == "X":
                    self.max_x = self.parse_x(words)
                elif self.command_word(words) == "Y":
                    self.max_y = self.parse_y(words)
                elif self.command_word(words) == "B":
                    self.blocks.add(self.parse_blocks(words))
                elif self.command_word(words) == "F":
                    self.fragile.append(self.parse_fragile(words))
                elif self.command_word(words) == "A":
                    self.aigent = self.parse_aigent(words)
                elif self.command_word(words) == "P":
                    self.packages.add(self.parse_pacakge(words))

        # Set the agent fragile to fragile edges
        self.aigent.fragile_edges = self.fragile

    def command_word(self, words: [str]) -> str:
        return words[0][1]

    def parse_x(self, words: [str]) -> int:
        return int(words[1])

    def parse_y(self, words: [str]) -> int:
        return int(words[1])

    def parse_blocks(self, words: [str]) -> Edge:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        return Edge(org_point, dst_point, 0)

    def parse_fragile(self, words: [str]) -> Edge:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        prob = float(words[5])
        return Edge(org_point, dst_point, prob)

    def parse_aigent(self, words: [str]) -> AiAigent:
        return AiAigent(Point(int(words[1]), int(words[2])), 0, None)

    def parse_pacakge(self, words: [str]) -> Package:
        org_point = Point(int(words[1]), int(words[2]))
        from_time = int(words[3])
        dst_point = Point(int(words[5]), int(words[6]))
        dead_line = int(7)
        return Package(org_point, from_time, dst_point, dead_line)
