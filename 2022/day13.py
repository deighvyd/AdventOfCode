import common
import functools

DAY = 13
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

def ComparePair(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return CompareInt(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        return CompareList(left, right)
    else:
        return CompareMixed(left, right)

def CompareInt(left, right) -> int:
    if left < right:
        return -1
    elif left > right:
        return 1
    else:
        return 0

def CompareList(left, right) -> int:
    for i in range(min(len(left), len(right))):
        result = ComparePair(left[i], right[i])
        if result == 0:
            continue
        else:
            return result

    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1
    else:
        return 0

def CompareMixed(left, right) -> int:
    if isinstance(left, int):
        left = [left]
    else:
        right = [right]

    return CompareList(left, right)

def GetResultOne(filename):
    input = common.ReadFile(filename)
    
    pairs = []
    currPair = []
    for line in input:
        if line == "":
            assert(len(currPair) == 2)
            pairs.append(currPair)
            currPair = []
        else:
            exec(f"currPair.append({line})")
            #currPair.append(exec(line))

    assert(len(currPair) == 2)
    pairs.append(currPair)
    currPair = []
    
    total = 0
    for i in range(0, len(pairs)):
        pair = pairs[i]
        if ComparePair(pair[0], pair[1]) == -1:
            total += (i + 1)

    return total

def GetResultTwo(filename):
    input = common.ReadFile(filename)
    
    pairs = []
    currPair = []
    for line in input:
        if line == "":
            assert(len(currPair) == 2)
            pairs.append(currPair[0])
            pairs.append(currPair[1])
            currPair = []
        else:
            exec(f"currPair.append({line})")
            #currPair.append(exec(line))

    assert(len(currPair) == 2)
    pairs.append(currPair[0])
    pairs.append(currPair[1])

    pairs.append([[2]])
    pairs.append([[6]])
    
    indices = []
    pairs.sort(key=functools.cmp_to_key(ComparePair))
    for i in range(0, len(pairs)):
        pair = pairs[i]

        if len(pair) == 1 and isinstance(pair[0], list) and len(pair[0]) == 1:
            if pair[0][0] == 2 or pair[0][0] == 6:
                indices.append(i + 1)

    return indices[0] * indices[1]


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
