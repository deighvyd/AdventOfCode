import common
import re

DAY = 5
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Stack:
    def __init__(self, inputIdx):
        self.inputIdx = inputIdx
        self.packages = []

    def pushPackage(self, package):
        self.packages.append(package)

    def popPackage(self):
        return self.packages.pop()

    def pushPackages(self, packages):
        for package in packages:
            self.packages.append(package)

    def popPackages(self, count):
        packages = self.packages[-count:]
        self.packages = self.packages[:-count]
        return packages

    def peekPackage(self):
        return self.packages[-1]

    def print(self):
        print(f"{self.inputIdx} {self.packages}")

def GetResultOne(filename):
    rawStacks = []
    moves = []

    current = rawStacks
    for line in common.ReadFile(filename):
        if line[-1] == '\n':
            line = line[:-1]

        if line == "":
            current = moves
        else:
            current.append(line)

    stacks = []
    
    rawStacks.reverse()
    stackDefs = rawStacks[0]
    for i in range(0, len(stackDefs)):
        char = stackDefs[i]
        if char != " ":
            stacks.append(Stack(i))

    for row in rawStacks[1:]:
        for stack in stacks:
            if (row[stack.inputIdx] != " "):
                stack.pushPackage(row[stack.inputIdx])

    ProcessMoves(stacks, moves)

    result = ""
    for stack in stacks:
        result = result + stack.peekPackage()

    return result

def ProcessMoves(stacks, moves):
    movePattern = re.compile(r'move (\d*) from (\d*) to (\d*)')
    for move in moves:
        match = movePattern.search(move)
        
        moveCount = int(match.group(1))
        sourceIdx = int(match.group(2)) - 1
        destIdx = int(match.group(3)) - 1
        for i in range(0, moveCount):
            package = stacks[sourceIdx].popPackage()
            stacks[destIdx].pushPackage(package)

def GetResultTwo(filename):
    rawStacks = []
    moves = []

    current = rawStacks
    for line in common.ReadFile(filename):
        if line[-1] == '\n':
            line = line[:-1]

        if line == "":
            current = moves
        else:
            current.append(line)

    stacks = []
    
    rawStacks.reverse()
    stackDefs = rawStacks[0]
    for i in range(0, len(stackDefs)):
        char = stackDefs[i]
        if char != " ":
            stacks.append(Stack(i))

    for row in rawStacks[1:]:
        for stack in stacks:
            if (row[stack.inputIdx] != " "):
                stack.pushPackage(row[stack.inputIdx])

    ProcessMovesMulti(stacks, moves)

    result = ""
    for stack in stacks:
        result = result + stack.peekPackage()

    return result

def ProcessMovesMulti(stacks, moves):
    movePattern = re.compile(r'move (\d*) from (\d*) to (\d*)')
    for move in moves:
        match = movePattern.search(move)
        
        moveCount = int(match.group(1))
        sourceIdx = int(match.group(2)) - 1
        destIdx = int(match.group(3)) - 1

        packages = stacks[sourceIdx].popPackages(moveCount)
        stacks[destIdx].pushPackages(packages)

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
