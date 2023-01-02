import common

DAY = 6
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

def GetResultOne(filename):
    stream = common.ReadFile(filename)[0].strip()
    
    count = 4
    buffer = stream[:4]
    stream = stream[4:]

    while not IsMarker(buffer):
        buffer = buffer[1:] + stream[:1]
        stream = stream[1:]
        count = count + 1
    
    return count

def IsMarker(buffer):
    for i in range(0, len(buffer)):
        for j in range(0, len(buffer)):
            if (i == j):
                continue
            if (buffer[i] == buffer[j]):
                return False
        
    return True

def GetResultTwo(filename):
    stream = common.ReadFile(filename)[0].strip()
    
    count = 14
    buffer = stream[:14]
    stream = stream[14:]

    while not IsMarker(buffer):
        buffer = buffer[1:] + stream[:1]
        stream = stream[1:]
        count = count + 1
    
    return count


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)}cre puzzle = {GetResultTwo(INPUT)}")
