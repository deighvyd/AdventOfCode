import os

def FollowPath(file):
    commands = []
    with open(file) as f:
        commands = f.readlines()

    x = 0
    y = 0
    for command in commands:
        parts = command.split(" ")
        match parts[0]:
            case "forward":
                x = x + int(parts[1])
            case "up":
                y = y - int(parts[1])
            case "down":
                y = y + int(parts[1])
            case _:
                print("unknown command")

    print(file + " x = " + str(x) + " y = " + str(y) + " (" + str(x * y) + ")")

def FollowAimPath(file):
    commands = []
    with open(file) as f:
        commands = f.readlines()

    x = 0
    y = 0
    aim = 0
    for command in commands:
        parts = command.split(" ")
        match parts[0]:
            case "forward":
                x = x + int(parts[1])
                y = y + (aim * int(parts[1]))
            case "up":
                aim = aim - int(parts[1])
            case "down":
                aim = aim + int(parts[1])
            case _:
                print("unknown command")

    print(file + " x = " + str(x) + " y = " + str(y) + " (" + str(x * y) + ")")

print("Part 1")
FollowPath("DayTwo/input_test.txt")
FollowPath("DayTwo/input.txt")

print("Part 2")
FollowAimPath("DayTwo/input_test.txt")
FollowAimPath("DayTwo/input.txt")