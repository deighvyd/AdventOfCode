import common

DAY = 4
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class SectionRange:
    def __init__(self, range):
        min, max = range.split('-')
        self.min, self.max = int(min), int(max)

    def contains(self, right):
        if (self.min <= right.min and self.max >= right.max):
            return True

        return False

    def overlaps(self, right):
        if (self.max < right.min or self.min > right.max):
            return False

        return True

def GetResultOne(filename):
    pairs = common.ReadFile(filename)

    overlapCount = 0

    sections = []
    for pair in pairs:
        sectionOne, sectionTwo = pair.split(',')
        rangeOne, rangeTwo = SectionRange(sectionOne), SectionRange(sectionTwo)
        if (rangeOne.contains(rangeTwo) or rangeTwo.contains(rangeOne)):
            overlapCount = overlapCount + 1
    
    return overlapCount

def GetResultTwo(filename):
    pairs = common.ReadFile(filename)

    overlapCount = 0

    sections = []
    for pair in pairs:
        sectionOne, sectionTwo = pair.split(',')
        rangeOne, rangeTwo = SectionRange(sectionOne), SectionRange(sectionTwo)
        if (rangeOne.overlaps(rangeTwo) or rangeTwo.overlaps(rangeOne)):
            overlapCount = overlapCount + 1
    
    return overlapCount


print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
