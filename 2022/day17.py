from __future__ import annotations

from collections import defaultdict

import common
from common import Point

DAY = 17
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Shape:
    def __init__(self, points: list[Point]) -> None:
        self.points: list[Point] = points
        self.position: Point = Point(2, 0)
        self.min: int = Point(float('inf'), float('inf'))
        self.max: int = Point(0, 0)
        for point in self.points:
            self.min.x = min(self.min.x, point.x)
            self.min.y = min(self.min.y, point.y)
            self.max.x = max(self.max.x, point.x)
            self.max.y = max(self.max.y, point.y)
        self.width: int = self.max.x - self.min.x + 1
        self.height: int = self.max.y - self.min.y + 1

    def __str__(self) -> str:
        result = f'{self.width}x{self.height} {self.min} {self.max}\n'
        for y in range(self.max.y, self.min.y - 1, -1):
            for x in range(self.min.x, self.max.x + 1):
                loc = Point(x, y)
                if loc in self.points:
                    result += '#'
                else:
                    result += '.'
            result += '\n'
        return result

    def containsPoint(self, point: Point) -> bool:
        for p in self.points:
            if (self.position + p) == point:
                return True

        return False

    def checkMoveRight(self, limit: int, rocks: set[Point]) -> bool:
        newPos = Point(self.position.x + 1, self.position.y)
        for point in self.points:
            pos = newPos + point
            if pos.x >= limit:
                return False
            elif pos in rocks:
                return False
        
        self.position = newPos
        return True

    def checkMoveLeft(self, limit: int, rocks: set[Point]) -> bool:
        newPos = Point(self.position.x - 1, self.position.y)
        for point in self.points:
            pos = newPos + point
            if pos.x < limit:
                return False
            elif pos in rocks:
                return False
        
        self.position = newPos
        return True

    def checkMoveDown(self, floor: int, rocks: set[Point]) -> bool:
        newPos = Point(self.position.x, self.position.y - 1)
        for point in self.points:
            pos = newPos + point
            if pos.y <= floor:
                return False
            elif pos in rocks:
                return False
        
        self.position = newPos
        return True
    
    def convertToRock(self, rocks: set[Point]) -> None:
        for point in self.points:
            rocks.add(self.position + point)

    def getMaxHeight(self) -> int:
        height = 0
        for point in self.points:
            pos = self.position + point
            if pos.y > height:
                height = pos.y
            
        return height

Shapes = [
    Shape([Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]),
    Shape([Point(1, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(1, 2)]),
    Shape([Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)]),
    Shape([Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)]),
    Shape([Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]),
]

class Chamber:
    Width: int = 7
    Floor: int = 0

    def __init__(self, gasses: str) -> None:
        self.height: int = 0
        self.gasses: str = gasses
        self.currGasIdx: int = 0
        self.rocks: set[Point] = set()
        #self.currShape: Shape = None
        #self.print()

    def print(self, shape: Shape = None):
        height = self.height + 10
        for i in range(height, 0, -1):
            line = f"{i:02d}: |"
            for j in range(0, Chamber.Width):
                pos = Point(j, i)
                if shape != None and shape.containsPoint(pos):
                    line += '@'
                elif pos in self.rocks:
                    line += '#'
                else:
                    line += '.'
            line += '|'
            print(line)
        
        print(f"{i:02d}: +-------+")

    def add(self, shape: Shape) -> None:
        shape.position = Point(2, self.height + 4)
        #self.print(shape)
        
        while True:
            # move the object by the gas
            match self.gasses[self.currGasIdx]:
                case '>':
                    shape.checkMoveRight(Chamber.Width, self.rocks)
                case '<':
                    shape.checkMoveLeft(0, self.rocks)
                case other:
                    print(f'error: unknown gas {self.gasses[self.currGasIdx]}')
            self.currGasIdx = (self.currGasIdx + 1) % len(self.gasses)

            # try to move down
            if not shape.checkMoveDown(Chamber.Floor, self.rocks):
                shape.convertToRock(self.rocks)
                self.height = max(self.rocks, key=lambda r: r.y).y
                #self.print(shape)
                break

            #self.print(shape)

def GetResultOne(filename):
    chamber = Chamber(common.ReadFile(filename)[0])

    # print(chamber,gasses)
    # for shape in Shapes:
    #     print(shape)

    currShapeIdx = 0
    for i in range (0, 2022):
        shape = Shapes[currShapeIdx]
        chamber.add(shape)
        currShapeIdx = (currShapeIdx + 1) % len(Shapes)

    return chamber.height

def GetResultTwo(filename):
    chamber = Chamber(common.ReadFile(filename)[0])

    # print(chamber,gasses)
    # for shape in Shapes:
    #     print(shape)

    cycleFound = False
    states = defaultdict(lambda: None)

    currShapeIdx = 0
    i = 0
    while i < 1000000000000:
    #for i in range (0, 1000000000000):
        #print(f"{i:013d}: {((i / 1000000000000) * 100):.1f}%", end='\r')

        preHeight = chamber.height
        
        shape = Shapes[currShapeIdx]
        chamber.add(shape)

        if not cycleFound:
            heights = []
            for j in range(0, Chamber.Width):
                maxHeight = 0
                for r in list(filter(lambda r: r.x == j, chamber.rocks)):
                    if r.y > maxHeight:
                        maxHeight = r.y
                heights.append(maxHeight)
            
            minCol = min(heights)
            relCols = [(h - minCol) for h in heights]
            relCols.extend([currShapeIdx, chamber.currGasIdx])
            state = tuple(relCols)

            if state in states:
                cycleFound = True

                cycleRocks = i - states[state]["rocks"]
                cycleHeights = chamber.height - states[state]["height"]
                
                rocksRemaining = 1000000000000 - i
                cyclesRemaining = rocksRemaining // cycleRocks
                rockRemainder = rocksRemaining % cycleRocks

                heightDiff = cycleHeights * cyclesRemaining
                i = 1000000000000 - rockRemainder
            else:
                states[state] = { "rocks": i, "height": chamber.height }
        
        currShapeIdx = (currShapeIdx + 1) % len(Shapes)
        i += 1

    return chamber.height + heightDiff

#print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
