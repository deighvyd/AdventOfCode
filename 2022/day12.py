import common
import sys

DAY = 12
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Location:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.height = -1

        self.reset()

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if other == None:
            return False

        return self.x == other.x and self.y == other.y

    def reset(self):
        self.g = 0
        self.h = sys.float_info.max
        self.open = False
        self.visited = False
        self.parent = None

    def canMove(self, dest):
        return dest.height <= (self.height + 1)

    def diff(self, loc) -> float:
        xDiff = abs(self.x - loc.x)
        yDiff = abs(self.y - loc.y)
        return (xDiff * xDiff) + (yDiff + yDiff)
       
class Map:
    Directions = ['u', 'd', 'l', 'r']

    def __init__(self, input) -> None:
        self.locations = []
        self.width = len(input[0])
        self.height = len(input)
        self.start = None
        self.end = None
        for row in range(0, self.height):
            for col in range(0, self.width):
                val = input[row][col]
                loc = Location(col, row, val)
                self.locations.append(loc)
                match val:
                    case 'S':
                        self.start = loc
                        loc.height = ord('a')
                    case 'E':
                        self.end = loc
                        loc.height = ord('z')
                    case other:
                        loc.height = ord(val)
                        pass

    def findPath(self, start=None) -> list[Location]:
        for loc in self.locations:
            loc.reset()
        
        if start == None:
            start = self.start

        start.open = True
        start.g = 0
        start.h = start.diff(self.end)
        open = [start]

        endNode = None
        while len(open) > 0 and endNode == None:
            curr = open.pop()
            curr.visited = True
            if curr == self.end:
                break

            for dir in Map.Directions:
                neighbour = self.__neighbour(curr, dir)
                if neighbour == None:
                    continue
                elif neighbour.visited:
                    continue
                elif not neighbour.open:
                    if curr.canMove(neighbour):
                        neighbour.g = curr.g + 1
                        neighbour.h = neighbour.diff(self.end)
                        neighbour.open = True
                        neighbour.parent = curr
                        open.append(neighbour)
                elif neighbour.open:
                    if curr.canMove(neighbour) and (curr.g + 1) <= neighbour.g:
                        neighbour.g = curr.g + 1
                        neighbour.parent = curr
            
            open.sort(key=lambda loc: (loc.g + loc.h), reverse=True)

        path = []
        curr = self.end
        while curr.parent != None:
            path.append(curr)
            curr = curr.parent
        path.reverse()
        return path

    def __neighbour(self, loc, direction) -> Location:
        match direction:
            case 'u':
                return self.location(loc.x, loc.y - 1)
            case 'd':
                return self.location(loc.x, loc.y + 1)
            case 'l':
                return self.location(loc.x - 1, loc.y)
            case 'r':
                return self.location(loc.x + 1, loc.y)
            case other:
                print(f"error: unknown direction '{direction}'")
                return None
    
    def __index(self, loc: Location) -> int:
        return (self.width * loc.y) + loc.x

    def location(self, x, y) -> int:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        
        return self.locations[(self.width * y) + x]

    def __str__(self) -> str:
        string = f'Map ({self.width} x {self.height}\n'
        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.location(col, row).val
            string += '\n'

        string += (f"Start - {self.start}\n")
        string += (f"End - {self.end}")

        return string

def GetResultOne(filename):
    map = Map(common.ReadFile(filename))
    path = map.findPath()
    # print(map.end.g)
    # print(map)
    if len(path) == 0:
        print('error: path not found')
    return len(path)

def GetResultTwo(filename):
    map = Map(common.ReadFile(filename))
    
    minPathLen = float('inf')
    for row in range(0, map.height):
        for col in range(0, map.width):
            if map.location(col, row).height == ord('a'):
                path = map.findPath(map.location(col, row))
                #if len(path) == 0:
                #    print('error: path not found')
                if len(path) > 0 and len(path) < minPathLen:
                    minPathLen = len(path)
    
    return minPathLen


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
