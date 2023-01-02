import common
import re

DAY = 7
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

COMMAND_PATTERN = re.compile(r'\$ (cd|ls) ?(.*)?')
FILE_PATTERN = re.compile(r'(\d?) (.*)')
DIR_PATTERN = re.compile(r'dir (.*)')

def GetIndentString(indent):
    indentStr = ''
    for i in range(0, indent):
        indentStr = indentStr + ' '
    return indentStr

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def Print(self, indent):
        print(f"{GetIndentString(indent)} {self.size} {self.name}")

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.directories = []

    def GetSize(self):
        size = 0
        for file in self.files:
            size = size + file.size
        for dir in self.directories:
            size = size + dir.GetSize()
        return size

    def Print(self, indent):
        print(f"{GetIndentString(indent)} dir {self.name}")
        for file in self.files:
            file.Print(indent + 1)
        for dir in self.directories:
            dir.Print(indent + 1)

class FileSystem:
    def __init__(self):
        self.root = Directory("root", None)
        self.current = self.root

    def Print(self):
        self.root.Print(0)

    def ExecuteCommand(self, command, input):
        match = COMMAND_PATTERN.search(command)
        cmd = match.group(1)
        match (cmd):
            case 'cd':
                dir = match.group(2)
                if (not self.__ChangeDir(dir)):
                    print(f"Error: could not change directory '{dir}'")
            case 'ls':
                self.__ListDir(input)

    def ForEachDirectory(self, visitor):
        self.__ForEachDirectory(self.root, visitor)

    def __ForEachDirectory(self, directory, visitor):
        for dir in directory.directories:
            visitor(dir)
            self.__ForEachDirectory(dir, visitor)

    def __ChangeDir(self, directory):
        match(directory):
            case '/':
                self.current = self.root
                return True
            case '..':
                self.current = self.current.parent
                return True
            case other:
                for dir in self.current.directories:
                    if dir.name == directory:
                        self.current = dir
                        return True
        
        return False

    def __ListDir(self, input):
        for item in input:
            parts = item.split(' ')
            if parts[0] == 'dir':
                dir = Directory(parts[1], self.current)
                self.current.directories.append(dir)
            else:
                file = File(parts[1], int(parts[0]))
                self.current.files.append(file)
                
def GetResultOne(filename):
    commands = common.ReadFile(filename)
    fileSys = FileSystem()

    idx = 0
    while idx < len(commands):
        command = commands[idx]
        input = []
        while (idx + 1) < len(commands) and commands[idx + 1][0] != '$':
            input.append(commands[idx + 1])
            idx = idx + 1
        fileSys.ExecuteCommand(command, input)
        idx = idx + 1

    eligibleDirs = []
    def visitor(dir):
        if (dir.GetSize() <= 100000):
            eligibleDirs.append(dir)
    fileSys.ForEachDirectory(visitor)

    totalSize = 0
    for dir in eligibleDirs:
        totalSize = totalSize + dir.GetSize()

    #fileSys.Print()
        
    return totalSize

def GetResultTwo(filename):
    commands = common.ReadFile(filename)
    fileSys = FileSystem()

    idx = 0
    while idx < len(commands):
        command = commands[idx]
        input = []
        while (idx + 1) < len(commands) and commands[idx + 1][0] != '$':
            input.append(commands[idx + 1])
            idx = idx + 1
        fileSys.ExecuteCommand(command, input)
        idx = idx + 1

    maxSize = 70000000
    requiredSize = 30000000
    currSize = fileSys.root.GetSize()
    freeSpace = maxSize - currSize
    needToFree = requiredSize - freeSpace

    selectedDir = None
    def visitor(dir):
        if (dir.GetSize() < needToFree):
            return

        nonlocal selectedDir

        if (selectedDir == None) or (dir.GetSize() < selectedDir.GetSize()):
            selectedDir = dir
    fileSys.ForEachDirectory(visitor)

    return selectedDir.GetSize()


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
