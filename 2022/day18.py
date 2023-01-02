from __future__ import annotations

import common
from Vector3 import *

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
        
        open = list(set(neghbours).difference(cubes))
        for n in open:
            ns = [n + Vector3.X, n - Vector3.X, n + Vector3.Y, n - Vector3.Y, n + Vector3.Z, n - Vector3.Z]
            if len(list(set(ns).difference(cubes))) > 0:
                faceCount += 1
        
        count += 1

    return faceCount

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
