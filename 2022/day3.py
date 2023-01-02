import common

DAY = 3
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

def GetResultOne(filename):
    rucksacks = common.ReadFile(filename)
    
    sum = 0
    for rucksack in rucksacks:
        sum = sum + GetPriority(rucksack.strip())
    
    return sum

def GetPriority(rucksack):
    compSize = int(len(rucksack) / 2)
    comp1 = rucksack[0:compSize]
    comp2 = rucksack[compSize:]

    duplicate = ""
    for item in comp1:
        if item in comp2:
            duplicate = item
            break

    return CalculatePriority(duplicate)

def CalculatePriority(item):
    priority = 0
    if item.islower():
        priority = ord(item) - 96
    else:
        priority = ord(item) - 38

    return priority

def GetResultTwo(filename):
    rucksacks = common.ReadFile(filename)
    
    sum = 0
    for group in range(0, len(rucksacks), 3):
        badge = GetBadge(rucksacks[group], rucksacks[group + 1], rucksacks[group + 2])
        sum = sum + CalculatePriority(badge)
        
    return sum

def GetBadge(one, two, three):
    for item in one:
        if item in two and item in three:
            return item

    return ""

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
