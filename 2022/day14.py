import common
from common import Point
from collections import defaultdict

DAY = 14
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class RockLine:
    def __init__(self, points) -> None:
        self.points = points

    def __str__(self) -> str:
        result = ""
        for i in range(0, len(self.points)):
            if i > 0:
                result += " -> "
            result += str(self.points[i])

        return result

    def intersects(self, point: Point) -> bool:
        for i in range(1, len(self.points)):
            if self.__intersectsLine(point, self.points[i - 1], self.points[i]):
                return True
                
        return False

    def __intersectsLine(self, point: Point, start: Point, end: Point) -> bool:
        if start.x == end.x:
            if end.y < start.y:
                start, end = end, start
            if point.y >= start.y and point.y <= end.y and point.x == start.x:
                return True
        elif start.y == end.y:
            if end.x < start.x:
                start, end = end, start
            if point.x >= start.x and point.x <= end.x and point.y == start.y:
                return True
        else:
            print("error: non parallel line")

        return False

class Simulation:
    StartPoint = Point(500, 0)
    def __init__(self, input) -> None:
        self.rockLines = []
        self.min = Point(float('inf'), float('inf'))
        self.max = Point(float('-inf'), float('-inf'))
        self.width = -1
        self.height = -1
        self.sand = None
        self.__updateBounds(Simulation.StartPoint)
        self.__read(input)

    def __read(self, input) -> None:
        for line in input:
            points = []
            for point in line.split(" -> "):
                parts = point.split(',')
                point = Point(int(parts[0]), int(parts[1]))
                points.append(point)

                self.__updateBounds(point)

            self.rockLines.append(RockLine(points))

        self.width = self.max.x - self.min.x + 1
        self.height = self.max.y - self.min.y + 1

        self.layout = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.layout.append('.')
        
        self.__paintPoint(Simulation.StartPoint, '+')
        for i in range(0, len(self.rockLines)):
            rockLine  = self.rockLines[i]
            for j in range(1, len(rockLine.points)):
                self.__paintLine(rockLine.points[j - 1], rockLine.points[j], '#')

    def __updateBounds(self, point) -> None:
        self.min.x = min(point.x, self.min.x)
        self.min.y = min(point.y, self.min.y)
        self.max.x = max(point.x, self.max.x)
        self.max.y = max(point.y, self.max.y)

    def __str__(self) -> str:
        result = f"{self.width}x{self.height}\n"
        result += f"{self.min}-{self.max}\n"

        written = 0
        for i in range(0, len(self.layout)):
            result += self.layout[i]
            if (i + 1) % self.width == 0:
                result += '\n'
            written = i
        print(written)

        for line in self.rockLines:
            result += f"{line}\n"
        
        return result

    def print(self) -> None:
        line = ""
        for i in range(0, len(self.layout)):
            x = self.min.x + int(i % self.width)
            y = self.min.y + int(i / self.width)
            point = Point(x, y)
            if self.sand != None and self.sand[str(point)]:
                line += 'o'
            else:
                line += self.layout[i]
            if (i + 1) % self.width == 0:
                print(line)
                line = ""

    def __paintPoint(self, point: Point, type: str) -> None:
        i, j = point.x - self.min.x, point.y - self.min.y
        self.layout[(self.width * j) + i] = type

    def __paintLine(self, start: Point, end: Point, type: str) -> None:
        if start.x == end.x:
            if end.y < start.y:
                start, end = end, start
            for y in range(start.y, end.y + 1):
                self.__paintPoint(Point(start.x, y), type)
        elif start.y == end.y:
            if end.x < start.x:
                start, end = end, start
            for x in range(start.x, end.x + 1):
                self.__paintPoint(Point(x, start.y), type)
        else:
            print("error: non parallel line")

    def __isRock(self, point: Point) -> bool:
        i, j = point.x - self.min.x, point.y - self.min.y
        return self.layout[(self.width * j) + i] == '#'

    def __isRockFill(self, point: Point) -> bool:
        i, j = point.x - self.min.x, point.y - self.min.y
        if j == (self.height - 1):
            return True
        if i < 0 or i >= self.width or j < 0 or j >= self.height:
            return False
        return self.layout[(self.width * j) + i] == '#'

    def __isRockSlow(self, point: Point) -> bool:
        for rockLine in self.rockLines:
            if rockLine.intersects(point):
                return True

    def __isSand(self, point: Point) -> bool:
        i, j = point.x - self.min.x, point.y - self.min.y
        return self.layout[(self.width * j) + i] == 'o'

    def __isSandSlow(self, point: Point) -> bool:
        return point in self.sand

    def addRow(self, type):
        for i in range(0, self.width):
            self.layout.append(type)
        self.height += 1

    def simulate(self):
        sandCount = 0
        finished = False
        while not finished:
            grain = Simulation.StartPoint.clone()
            while True:
                nextPos = grain.clone()
                nextPos.y += 1
                if nextPos.y >= self.height:
                    finished = True
                    break

                if not self.__isRock(nextPos) and not self.__isSand(nextPos):
                    grain = nextPos
                    continue
                
                nextPos.x -= 1
                if nextPos.x < self.min.x or nextPos.x > self.max.x:
                    finished = True
                    break
                elif not self.__isRock(nextPos) and not self.__isSand(nextPos):
                    grain = nextPos
                    continue

                nextPos.x += 2
                if nextPos.x < self.min.x or nextPos.x > self.max.x:
                    finished = True
                    break
                elif not self.__isRock(nextPos) and not self.__isSand(nextPos):
                    grain = nextPos
                    continue

                self.__paintPoint(grain, 'o')
                sandCount += 1
                #print(self)
                break

        return sandCount

    def simulateSlow(self):
        sandCount = 0
        self.sand = defaultdict(lambda: False)
        finished = False
        while not finished:
            grain = Simulation.StartPoint.clone()
            while True:
                nextPos = grain.clone()
                nextPos.y += 1
                if nextPos.y >= self.height:
                    finished = True
                    break

                if not self.__isRock(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue
                
                nextPos.x -= 1
                if nextPos.x < self.min.x or nextPos.x > self.max.x:
                    finished = True
                    break
                elif not self.__isRock(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue

                nextPos.x += 2
                if nextPos.x < self.min.x or nextPos.x > self.max.x:
                    finished = True
                    break
                elif not self.__isRock(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue

                #self.__paintPoint(grain, 'o')
                self.sand[str(grain)] = True
                #self.sand.append(grain)
                sandCount += 1
                #self.print()
                #print(self)
                break

        return sandCount

    def simulateFill(self):
        sandCount = 0
        self.sand = defaultdict(lambda: False)
        finished = False
        while not finished:
            grain = Simulation.StartPoint.clone()
            while True:
                nextPos = grain.clone()
                nextPos.y += 1
                # if nextPos.y >= self.height:
                #     finished = True
                #     break

                if not self.__isRockFill(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue
                
                nextPos.x -= 1
                # if nextPos.x < self.min.x or nextPos.x > self.max.x:
                #     finished = True
                #     break
                if not self.__isRockFill(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue

                nextPos.x += 2
                # if nextPos.x < self.min.x or nextPos.x > self.max.x:
                #     finished = True
                #     break
                if not self.__isRockFill(nextPos) and not self.sand[str(nextPos)]: #self.__isSandSlow(nextPos):
                    grain = nextPos
                    continue

                if grain == Simulation.StartPoint:
                    finished = True
                    break
                #self.__paintPoint(grain, 'o')
                self.sand[str(grain)] = True
                #self.sand.append(grain)
                sandCount += 1
                #self.print()
                #print(self)
                break

        return sandCount + 1

def GetResultOne(filename):
    sim = Simulation(common.ReadFile(filename))
    #sim.print()
    return sim.simulateSlow()

def GetResultTwo(filename):
    sim = Simulation(common.ReadFile(filename))
    sim.addRow('.')
    sim.addRow('#')
    #sim.print()
    return sim.simulateFill()


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
