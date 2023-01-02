import common

DAY = 8
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Map:
    def __init__(self, input) -> None:
        self.rows = []
        self.width = -1
        self.height = -1
        self.__read(input)

    def __read(self, input):
        for rowIdx in range(0, len(input)):
            if self.width < 0:
                self.width = len(input[rowIdx])
            else:
                assert self.width == len(input[rowIdx])

            self.rows.append([])
            for column in input[rowIdx]:
                self.rows[rowIdx].append(int(column))
        
        self.height = len(self.rows)

    def visibleCount(self):
        count = (self.width * 2) + (self.height * 2) - 4
        for rowIdx in range(1, self.height - 1):
            for colIdx in range(1, self.width - 1):
                visibleTop = self.__isVisible(rowIdx, colIdx, 'top') 
                visibleBottom = self.__isVisible(rowIdx, colIdx, 'bottom')
                visibleLeft = self.__isVisible(rowIdx, colIdx, 'left')
                visibleRight = self.__isVisible(rowIdx, colIdx, 'right')

                if (visibleTop or visibleBottom or visibleRight or visibleLeft):
                    count += 1

        return count

    def sceneicScore(self):
        bestScore = 0
        for rowIdx in range(1, self.height - 1):
            for colIdx in range(1, self.width - 1):
                scoreTop = self.__scenicScore(rowIdx, colIdx, 'top') 
                scoreBottom = self.__scenicScore(rowIdx, colIdx, 'bottom')
                scoreLeft = self.__scenicScore(rowIdx, colIdx, 'left')
                scoreRight = self.__scenicScore(rowIdx, colIdx, 'right')

                score = (scoreTop * scoreBottom * scoreLeft * scoreRight)
                if (score > bestScore):
                    bestScore = score

        return bestScore

    def __scenicScore(self, row, column, direction):
        score = 0
        height = self.rows[row][column]
        match (direction):
            case 'top':
                for rowIdx in range(row - 1, -1, -1):
                    score += 1
                    if (self.rows[rowIdx][column] >= height):
                        break
            case 'bottom':
                for rowIdx in range(row + 1, self.height, 1):
                    score += 1
                    if (self.rows[rowIdx][column] >= height):
                        break
            case 'left':
                for colIdx in range(column - 1, -1, -1):
                    score += 1
                    if (self.rows[row][colIdx] >= height):
                        break
            case 'right':
                for colIdx in range(column + 1, self.width, 1):
                    score += 1
                    if (self.rows[row][colIdx] >= height):
                        break
            case other:
                print(f"error unknown direction {direction}")

        return score

    def __isVisible(self, row, column, direction):
        height = self.rows[row][column]
        match (direction):
            case 'top':
                for rowIdx in range(row - 1, -1, -1):
                    if (self.rows[rowIdx][column] >= height):
                        return False
            case 'bottom':
                for rowIdx in range(row + 1, self.height, 1):
                    if (self.rows[rowIdx][column] >= height):
                        return False
            case 'left':
                for colIdx in range(column - 1, -1, -1):
                    if (self.rows[row][colIdx] >= height):
                        return False
            case 'right':
                for colIdx in range(column + 1, self.width, 1):
                    if (self.rows[row][colIdx] >= height):
                        return False
            case other:
                print(f"error unknown direction {direction}")

        return True

    def print(self):
        for row in self.rows:
            rowStr = ''
            for column in row:
                rowStr += str(column)
            print(rowStr)

def GetResultOne(filename):
    mapInput = common.ReadFile(filename)
    map = Map(mapInput)
    #map.print()
    return map.visibleCount()

def GetResultTwo(filename):
    mapInput = common.ReadFile(filename)
    map = Map(mapInput)
    #map.print()
    return map.sceneicScore()


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
