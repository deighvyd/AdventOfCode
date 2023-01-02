import common

DAY = 2
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

def CalculateTotalScore(filename):
    rounds = common.ReadFile(filename)

    totalScore = 0
    for round in rounds:
        totalScore = totalScore + GetResultScore(round[0], round[2]) + GetHandScore(round[2])

    return totalScore

def CalculateTotalScore2(filename):
    rounds = common.ReadFile(filename)

    totalScore = 0
    for round in rounds:
        required = GetRequiredResult(round[0], round[2])
        totalScore = totalScore + GetResultScore(round[0], required) + GetHandScore(required)

    return totalScore

def GetRequiredResult(left, result):
    match left:
        case "A":
            match result:
                case "X":
                    return "Z"
                case "Y":
                    return "X"
                case "Z":
                    return "Y"
        case "B":
            match result:
                case "X":
                    return "X"
                case "Y":
                    return "Y"
                case "Z":
                    return "Z"
        case "C":
            match result:
                case "X":
                    return "Y"
                case "Y":
                    return "Z"
                case "Z":
                    return "X"

    return 0

def GetResultScore(left, right):
    match left:
        case "A":
            match right:
                case "X":
                    return 3
                case "Y":
                    return 6
                case "Z":
                    return 0
        case "B":
            match right:
                case "X":
                    return 0
                case "Y":
                    return 3
                case "Z":
                    return 6
        case "C":
            match right:
                case "X":
                    return 6
                case "Y":
                    return 0
                case "Z":
                    return 3

    return 0

def GetHandScore(hand):
    match hand:
        case "X":
            return 1
        case "Y":
            return 2
        case "Z":
            return 3

    return 0

print(f"Day {DAY}.1: test = {CalculateTotalScore(INPUT_TEST)} puzzle = {CalculateTotalScore(INPUT)}")
print(f"Day {DAY}.2: test = {CalculateTotalScore2(INPUT_TEST)} puzzle = {CalculateTotalScore2(INPUT)}")
