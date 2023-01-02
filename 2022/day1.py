import common

def GetMaxCalories(filename):
    values = common.ReadFile(filename)

    sum = 0
    max = 0
    for value in values:
        try:
            calories = int(value)
            sum = sum + calories
        except ValueError:
            if sum > max:
                max = sum
            sum = 0

    return max

def GetTopThreeMaxCalories(filename):
    values = common.ReadFile(filename)

    sum = 0
    maxValues = []
    for value in values:
        try:
            calories = int(value)
            sum = sum + calories
        except ValueError:
            maxValues.append(sum)
            sum = 0
    maxValues.append(sum)

    maxValue = maxValues.sort(reverse=True)
    return maxValues[0] + maxValues[1] + maxValues[2]



print("Day 1.1: test = " + str(GetMaxCalories("day1.input.test")) + " puzzle = " + str(GetMaxCalories("day1.input")))
print("Day 1.2: test = " + str(GetTopThreeMaxCalories("day1.input.test")) + " puzzle = " + str(GetTopThreeMaxCalories("day1.input")))
