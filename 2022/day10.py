import common

DAY = 10
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Instruction:
    def __init__(self, instruction) -> None:
        if ' ' in instruction:
            self.op, self.input = instruction.split(' ')
        else:
            self.op = instruction

        match (self.op):
            case 'noop':
                self.cycles = 1
            case 'addx':
                self.cycles = 2
            case other:
                print(f"error: unknown operation {self.op}")

    def execute(self) -> bool:
        self.cycles -= 1
        return self.cycles == 0

class CPU:
    def __init__(self) -> None:
        self.xReg = 1
        self.pc = 0
        self.cycle = 0
        self.instruction = None
        self.onCycle = None
        self.onCycleEnd = None

    def execute(self, instructions):
        while (self.pc < len(instructions)):
            if (self.instruction == None):
                self.instruction = Instruction(instructions[self.pc])

            self.cycle += 1
            if (self.onCycle != None):
                self.onCycle(self.cycle)

            if (self.instruction.execute()):
                if (self.instruction.op == 'addx'):
                    self.xReg += int(self.instruction.input)
                self.pc += 1
                self.instruction = None
            
            if (self.onCycleEnd != None):
                self.onCycleEnd(self.cycle)

class CRT:
    RowSize = 40
    def __init__(self) -> None:
        self.pixel = 0
        self.buffer = ''

    def draw(self, sprite):
        if (abs((self.pixel % CRT.RowSize) - sprite) <= 1):
            self.buffer += '#'
        else:
            self.buffer += '.'
        
        self.pixel += 1
        if (self.pixel % CRT.RowSize == 0):
            print(self.buffer)
            self.buffer = ''
        
def GetResultOne(filename):
    instructions = common.ReadFile(filename)
    
    cpu = CPU()
    sampleAtCycles = [20, 60, 100, 140, 180, 220]
    signalStrength = 0
    def onCycle(cycle):
        nonlocal signalStrength
        if cycle in sampleAtCycles:
            signalStrength += cycle * cpu.xReg

    cpu.onCycle = onCycle
    cpu.execute(instructions)
    
    return signalStrength

def GetResultTwo(filename):
    instructions = common.ReadFile(filename)
    
    cpu = CPU()
    crt = CRT()
    def onCycle(cycle):
        nonlocal crt, cpu
        crt.draw(cpu.xReg)

    separator = ''
    for i in range(0, CRT.RowSize):
        separator += '-'
    print(separator)
    
    cpu.onCycle = onCycle
    cpu.execute(instructions)
    
    return 0


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
