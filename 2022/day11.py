import common
import math
import re

DAY = 11
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Operation:
    def __init__(self, op, left, right) -> None:
        self.op = op
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"Operation: new = {self.left} {self.op} {self.right}"

    def execute(self, old) -> int:
        left = old if self.left == 'old' else int(self.left)
        right = old if self.right == 'old' else int(self.right)

        match self.op:
            case '+':
                return left + right
            case '*':
                return left * right
            case other:
                print(f"error: unknown operation {self.op}")
                return 0

class Test:
    def __init__(self, divisibleBy, trueMonkey, falseMonkey) -> None:
        self.divisibleBy = divisibleBy
        self.trueMonkey = trueMonkey
        self.falseMonkey = falseMonkey

    def __str__(self):
        return f"if worry / {self.divisibleBy} == 0\n  throw to monkey {self.trueMonkey}\n  throw to monkey {self.falseMonkey}"
    
    def execute(self, item) -> int:
        if item % self.divisibleBy == 0:
            return self.trueMonkey
        else:
            return self.falseMonkey

class Monkey:
    ItemsPatten = re.compile(r"Starting items: (.*)")
    OperationPattern = re.compile(r"Operation: new = (.*) (.*) (.*)") 
    
    TestPattern = re.compile(r"Test: divisible by (\d*)");
    TestResultPattern = re.compile(r"If (.*): throw to monkey (\d*)")

    def __init__(self, definition) -> None:
        self.__readItems(definition[1])
        self.__readOperation(definition[2])
        self.__readTest(definition[3], definition[4], definition[5])

        self.inspectedCount = 0

    def __readItems(self, itemsDefinition):
        match = Monkey.ItemsPatten.search(itemsDefinition)
        if match == None:
            print(f"error: error parsing items input {itemsDefinition}")
            return

        self.items = []
        for item in match.group(1).split(', '):
            self.items.append(int(item))

    def __readOperation(self, opDefinition):
        match = Monkey.OperationPattern.search(opDefinition)
        if match == None:
            print(f"error: error parsing operation input {opDefinition}")
            return

        self.operation = Operation(match.group(2), match.group(1), match.group(3))
    
    def __readTest(self, testDefinition, trueDefinition, falseDefinition):
        match = Monkey.TestPattern.search(testDefinition)
        if match == None:
            print(f"error: error parsing test input {testDefinition}")
            return
        divisibleBy = int(match.group(1))
        
        match = Monkey.TestResultPattern.search(trueDefinition)
        if match == None:
            print(f"error: error parsing test input {testDefinition}")
            return
        trueMonkey = int(match.group(2))

        match = Monkey.TestResultPattern.search(falseDefinition)
        if match == None:
            print(f"error: error parsing test input {testDefinition}")
            return
        falseMonkey = int(match.group(2))
        
        self.test = Test(divisibleBy, trueMonkey, falseMonkey)

    def catch(self, item) -> None:
        self.items.append(item)

    def inspect(self, reduceWorry=True, lcm=1) -> tuple[int, int]:
        if len(self.items) == 0:
            return -1, -1

        item = self.items[:1][0]
        self.items = self.items[1:]

        newItem = self.operation.execute(item)
        if reduceWorry:
            newItem = int(newItem / 3)
        elif newItem > lcm:
            newItem = newItem % lcm
            
        destMonkey = self.test.execute(newItem)

        self.inspectedCount += 1

        return newItem, destMonkey
    
    def print(self) -> str:
        items = 'Items: '
        for i in range(0, len(self.items)):
            if (i != 0):
                items += ', '
            item = self.items[i]
            items += str(item)
        print(items)
        print(self.operation)
        print(self.test)

def ReadMonkeys(input) -> list[Monkey]:
    monkeys = []

    monkeyInput = []
    for line in input:
        if (line != ''):
            monkeyInput.append(line)
        else:
            monkeys.append(Monkey(monkeyInput))
            monkeyInput = []
    monkeys.append(Monkey(monkeyInput))

    return monkeys

def GetResultOne(filename):
    input = common.ReadFile(filename)
    
    monkeys = ReadMonkeys(input)
    for round in range(0, 20):
        for monkey in monkeys:
            item, dest = monkey.inspect()
            while (item >= 0):
                monkeys[dest].catch(item)
                item, dest = monkey.inspect()    

        #print(f"round {round + 1}")
        # for monkey in monkeys:
        #     monkey.print()
    
    inspected = []
    for monkey in monkeys:
        inspected.append(monkey.inspectedCount)
    inspected.sort(reverse=True)

    #print(inspected)
    return inspected[0] * inspected[1]

def GetResultTwo(filename):
    input = common.ReadFile(filename)
    
    checkRounds = [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 9000, 10000]

    monkeys = ReadMonkeys(input)
    
    factors = []
    for monkey in monkeys:
        factors.append(monkey.test.divisibleBy)
    lcm = math.lcm(*factors)

    for round in range(0, 10000):
        print(f'Round: {round + 1}', end='\r')
        for monkey in monkeys:
            item, dest = monkey.inspect(reduceWorry=False, lcm=lcm)
            while (item >= 0):
                monkeys[dest].catch(item)
                item, dest = monkey.inspect(reduceWorry=False, lcm=lcm)    

        if (round + 1) in checkRounds:
            inspected = []
            for monkey in monkeys:
                inspected.append(monkey.inspectedCount)
            print(f"Round {round + 1} = {inspected}")
    
    inspected = []
    for monkey in monkeys:
        inspected.append(monkey.inspectedCount)
    inspected.sort(reverse=True)

    return inspected[0] * inspected[1]


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
#print(f"Day {DAY}.2: puzzle = {GetResultTwo(INPUT)}")
