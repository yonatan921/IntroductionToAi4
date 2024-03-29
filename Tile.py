from name_tuppels import Point


class Tile:
    def __init__(self, point: Point):
        self.point = point
        self.symbol = "."

    def __str__(self):
        return self.symbol.ljust(2) + " "

    def __eq__(self, other):
        return self.point == other.point and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.point.x, self.point.y, self.symbol))


class Package(Tile):
    def __init__(self, point: Point, from_time, point_dst, dead_line):
        super().__init__(point)
        self.from_time = from_time
        self.point_dst = point_dst
        self.dead_line = dead_line
        self.picked_up = False
        self.symbol = "P"

    def to_string(self):
        return f"pick up location:{self.point}, destination:{self.point_dst}"
