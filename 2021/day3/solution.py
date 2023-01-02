import os

def CalculatePower(file):
    inputs = []
    with open(file) as f:
        inputs = f.readlines()

    bitCounts = []

    for input in inputs:
        i = 0
        for char in input.rstrip('\n'):
            if (i == len(bitCounts)):
                bitCounts.append([0, 0])

            bitCounts[i][int(char)] = bitCounts[i][int(char)] + 1
            i = i + 1

    gamma = ''
    epsilon = ''
    for bitCount in bitCounts:
        if bitCount[0] > bitCount[1]:
            gamma = gamma + '0'
            epsilon = epsilon + '1'
        else:
            gamma = gamma + '1'
            epsilon = epsilon + '0'

    power = int(gamma, 2) * int(epsilon, 2)
    print('power = (' + gamma + '=' + str(int(gamma, 2)) + ') * (' + epsilon + '=' + str(int(epsilon, 2)) + ') = ' + str(power))

def FilterInputs(inputs, mostSignificant):
    bit = 0
    while len(inputs) > 1:
        bitCount = [0, 0]
        for input in inputs:
            bitCount[int(input[bit])] = bitCount[int(input[bit])] + 1
        
        outputs = []
        signifcantBit = str(0 if bitCount[0] > bitCount[1] else 1) if mostSignificant else str(0 if bitCount[0] <= bitCount[1] else 1)
        for input in inputs:
            if input[bit] == signifcantBit:
                outputs.append(input.rstrip('\n'))

        inputs = outputs
        bit = bit + 1

    return inputs[0]

def CalculateLifeSupport(file):
    inputs = []
    with open(file) as f:
        inputs = f.readlines()

    oxygen = FilterInputs(inputs, True)
    co2 = FilterInputs(inputs, False)

    lifeSupport = int(oxygen, 2) * int(co2, 2)
    print('life support = (' + oxygen + '=' + str(int(oxygen, 2)) + ') * (' + co2 + '=' + str(int(co2, 2)) + ') = ' + str(lifeSupport))

os.chdir('day3')

print("Part 1")
CalculatePower("input_test.txt")
CalculatePower("input.txt")

print("Part 2")
CalculateLifeSupport("input_test.txt")
CalculateLifeSupport("input.txt")