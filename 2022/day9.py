import common

DAY = 9
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def move(self, dir):
        match (dir):
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1
            case 'L':
                self.x -= 1
            case 'R':
                self.x += 1
            case other:
                print(f"error: unknown direction {dir}")

    def print(self):
        print(self.str())

    def str(self):
        return f"({self.x},{self.y})"

def FollowKnot(lead, follow):
    xDiff = abs(lead.x - follow.x)
    yDiff = abs(lead.y - follow.y)

    #assert xDiff < 2 or yDiff < 2

    # coninue if the tail does not need to move
    if (xDiff <= 1) and (yDiff <= 1):
        return

    if xDiff == 2:
        if follow.x < lead.x:
            follow.move('R')
        else:
            follow.move('L')

        if yDiff > 0:
            if follow.y < lead.y:
                follow.move('U')
            else:
                follow.move('D')
    elif yDiff == 2:
        if follow.y < lead.y:
            follow.move('U')
        else:
            follow.move('D')

        if xDiff > 0:
            if follow.x < lead.x:
                follow.move('R')
            else:
                follow.move('L')

def GetResultOne(filename):
    head = Position(0, 0)
    tail = Position(0, 0)
    
    visited = {}
    visited[tail.str()] = True

    moves = common.ReadFile(filename)
    for move in moves:
        dir, dist = move.split(' ')
        dist = int(dist)

        for i in range(0, dist):
            head.move(dir)
            FollowKnot(head, tail)
            visited[tail.str()] = True

    return len(visited.keys())

def GetResultTwo(filename):
    rope = []
    for i in range(0, 10):
        rope.append(Position(0, 0))
    
    visited = {}
    visited[rope[-1].str()] = True

    moves = common.ReadFile(filename)
    for move in moves:
        dir, dist = move.split(' ')
        dist = int(dist)

        for i in range(0, dist):
            rope[0].move(dir)
            for j in range(1, len(rope)):
                FollowKnot(rope[j - 1], rope[j])
            visited[rope[-1].str()] = True
            # for pos in rope:
            #     print(pos.str())
            # print("-----")
        
        #rope.reverse()
        #for pos in rope:
        #    print(pos.str())
        #print("-----")
        #rope.reverse()

    return len(visited.keys())

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
