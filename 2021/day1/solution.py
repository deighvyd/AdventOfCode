import os

def CountIncreases(file):
    values = []
    with open(file) as f:
        values = f.readlines()

    increases = 0
    previous = -1
    for line in values:
        if previous >= 0 and int(line) > previous:
            increases = increases + 1
        previous = int(line)

    print(file + " contains " + str(increases) + " increases")

def CountIncreasesWindow(file):
    values = []
    with open(file) as f:
        values = f.readlines()

    increases = 0
    previous = -1
    numValues = len(values)
    for i in range(0, numValues, 1):
        if i == numValues - 2:
            break

        value = int(values[i]) + int(values[i + 1]) + int(values[i + 2])
        if previous >= 0 and value > previous:
            increases = increases + 1
        previous = value

    print(file + " contains " + str(increases) + " increases")

print("Part 1")
CountIncreases("DayOne/input_test.txt")
CountIncreases("DayOne/input.txt")

print("Part 2")
CountIncreasesWindow("DayOne/input_test.txt")
CountIncreasesWindow("DayOne/input.txt")