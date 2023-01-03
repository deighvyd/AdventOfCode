from __future__ import annotations

import common
from math3d import *

DAY = 18
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

def GetResultOne(filename):
    cubes = []
    for line in common.ReadFile(filename):
        (x, y, z) = line.split(',')
        cubes.append(Vector3(int(x), int(y), int(z)))

    # for cube in cubes:
    #     print(cube)

    faceCount = 0

    count = 0
    for cube in cubes:
        print(f"{count:02d}: {((count / len(cubes)) * 100):.1f}%", end='\r')
        neghbours = [cube + Vector3.X, cube - Vector3.X, cube + Vector3.Y, cube - Vector3.Y, cube + Vector3.Z, cube - Vector3.Z]
        faceCount += len(list(set(neghbours).difference(cubes)))
        count += 1

    return faceCount

def GetResultTwo(filename):
    cubes = []
    bounds = Bounds3()
    for line in common.ReadFile(filename):
        (x, y, z) = line.split(',')
        cube = Vector3(int(x), int(y), int(z))
        cubes.append(cube)
        bounds.expand(cube)
    bounds.expand(bounds.min - Vector3.One)
    bounds.expand(bounds.max + Vector3.One)

    # for cube in cubes:
    #     print(cube)

    open = [bounds.min]
    visited = set()
    pairs = set()
    while len(open) > 0:
        print(f"{len(open)}", end='\r')
        curr = open.pop()
        
        neighbours = [curr + Vector3.X, curr - Vector3.X, curr + Vector3.Y, curr - Vector3.Y, curr + Vector3.Z, curr - Vector3.Z]
        surfaceFaces = list(set(neighbours).intersection(cubes))
        for n in neighbours:
            if not bounds.contains(n) or n in visited:
                continue
                
            if n in cubes:
                pairs.add((curr, n))
            else:
                open.append(n)

        visited.add(curr)

    return len(pairs)

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
