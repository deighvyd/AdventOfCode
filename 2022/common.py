from __future__ import annotations

def ReadFile(filename):
    lines = []
    with open(filename) as f:
        for index, line in enumerate(f):
            lines.append(line.strip())
    
    return lines

class Point:
    Zero: Point
    One: Point
    X: Point
    Y: Point

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self) -> int:
        return hash(str(self))

    def dist(self, other) -> int:
        diff = self - other
        return abs(diff.x) + abs(diff.y)

    def clone(self):
        return Point(self.x, self.y)

class Range:
    def __init__(self, min: int, max: int) -> None:
        assert(min <= max)
        self.min = min
        self.max = max

    def __str__(self) -> str:
        return f"[{self.min} -> {self.max}]({self.size()})"

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        
        return self.min == other.min and self.max == other.max

    def size(self) -> int:
        return (self.max - self.min) + 1

    def intersects(self, other) -> bool:
        if abs(self.max - other.min) == 1 or abs(other.max - self.min) == 1:
            return True
            
        return self.min <= other.max and other.min <= self.max
        #return max(self.min, other.min) <= min(self.max, other.max)

    def merge(self, other):
        return Range(min(self.min, other.min), max(self.max, other.max))

Point.Zero = Point(0, 0)
Point.One = Point(1, 1)
Point.X = Point(1, 0)
Point.Y = Point(0, 1)

class Bounds:
    def __init__(self) -> None:
        self.min = Point(float('inf'), float('inf'))
        self.max = Point(float('-inf'), float('-inf'))
        self.width = -1
        self.height = -1

    def expand(self, point: Point) -> None:
        self.min.x = min(point.x, self.min.x)
        self.min.y = min(point.y, self.min.y)
        self.max.x = max(point.x, self.max.x)
        self.max.y = max(point.y, self.max.y)

        self.width = self.max.x - self.min.x + 1
        self.height = self.max.y - self.min.y + 1

    def forEach(self, visitor, data) -> None:
        if visitor == None:
            return

        for i in range(0, self.height):
            for j in range(0, self.width):
                loc = Point(self.min.x + j, self.min.y + i)
                visitor(i, j, loc, data)