import common
from common import *

import re

DAY = 15
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Sensor:
    def __init__(self, pos: Point, beacon: Point) -> None:
        self.position = pos
        self.beacon = beacon

    def beaconDist(self) -> int:
        return self.position.dist(self.beacon)

    def locDist(self, loc: Point) -> Point:
        return self.position.dist(loc)

    def test(self, loc: Point) -> bool:
        if self.beacon == loc:
            return False

        if self.locDist(loc) <= self.beaconDist():
            return True

        return False

    def testY(self, y: float, results: dict[str, str]) -> None:
        beaconDist = self.beaconDist()
        if abs(self.position.y - y) > beaconDist:
            return

        for x in range(self.position.x - beaconDist, self.position.x + beaconDist):
            loc = Point(x, y)
            if loc == self.beacon:
                results[str(loc)] = 'B'
            elif self.test(loc):
                results[str(loc)] = '#'

    def intersectY(self, y: float, clamp: Range = None) -> Range:
        beaconDist = self.beaconDist()

        yDiff = abs(self.position.y - y)
        if yDiff > beaconDist:
            return None

        xDiff = beaconDist - yDiff
        if clamp != None:
            return Range(max(self.position.x - xDiff, clamp.min), min(self.position.x + xDiff, clamp.max))
        else:
            return Range(self.position.x - xDiff, self.position.x + xDiff)

SensorPattern = re.compile(r"Sensor at x=(-?\d*), y=(-?\d*): closest beacon is at x=(-?\d*), y=(-?\d*)")

def GetResultOne(filename, y: int):
    sensors: list[Sensor] = []
    beacons: list[Point] = []
    map = Bounds()

    input = common.ReadFile(filename)
    for line in input:
        match = SensorPattern.search(line)
        beaconLoc = Point(int(match.group(3)), int(match.group(4)))
        map.expand(beaconLoc)
        beacons.append(beaconLoc)

        sensorLoc = Point(int(match.group(1)), int(match.group(2)))
        map.expand(sensorLoc)
        sensor = Sensor(sensorLoc, beaconLoc)
        sensors.append(sensor)

    for sensor in sensors:
        beaconDist = sensor.beaconDist()
        #print(f"{beaconDist} - {sensor.position} {sensor.beacon}")
        map.expand(Point(sensor.position.x + beaconDist, sensor.position.y))
        map.expand(Point(sensor.position.x - beaconDist, sensor.position.y))
        map.expand(Point(sensor.position.x, sensor.position.y + beaconDist))
        map.expand(Point(sensor.position.x, sensor.position.y - beaconDist))
    
    def mapPrinterSingle(i: int, j: int, loc: Point, data: any):
        #print(f"{i}, {j}")
        if j == 0 and i != 0:
            print('\n', end='')

        if j == 0:
            print(f"{loc.y:03d}:", end='')

        if beacons.count(loc) > 0:
            print('B', end='')
        elif sum(s.position == loc for s in sensors) > 0:
            print('S', end='')
        else:
            if data != None and data.test(loc):
                print('#', end='')
            else:
                print('.', end='')

    def mapPrinterMulti(i: int, j: int, loc: Point, data: any):
        if loc.x < 0 or loc.x > 20 or loc.y < 0 or loc.y > 20:
            return

        #print(f"{i}, {j}")
        if (j == 0 and i != 0) or loc.x == 0:
            print('\n', end='')

        if j == 0:
            print(f"{loc.y:03d}:", end='')

        if beacons.count(loc) > 0:
            print('B', end='')
        elif sum(s.position == loc for s in sensors) > 0:
            print('S', end='')
        else:
            if data != None:
                for sensor in data:
                    if sensor.test(loc):
                        print('#', end='')
                        return
            
            print('.', end='')

    #print(f"{map.width}x{map.height}, {map.min} {map.max}")
    
    # for sensor in sensors:
    #     map.forEach(mapPrinterSingle, sensor)
    #     print('\n', end='')

    #map.forEach(mapPrinterMulti, sensors)
    #print('\n', end='')

    # results = {}
    # for sensor in sensors:
    #     sensor.testY(y, results)

    # return sum(value == '#' for value in results.values())
    
    # for x in range(0, map.width):
    #     loc = Point(map.min.x + x, y)
    #     for sensor in sensors:
    #         if sensor.test(loc):
    #             test[x] = True
    
    # return test.count(True)
    
    ranges = []
    foundBeacons = []
    for sensor in sensors:
        range = sensor.intersectY(y)
        if range != None:
            ranges.append(range)
            ranges = MergeRanges(ranges)

        if sensor.beacon.y == y and foundBeacons.count(sensor.beacon) == 0:
            foundBeacons.append(sensor.beacon)

        #print(range)
        #map.forEach(mapPrinterSingle, sensor)
        #print('\n', end='')

    total = 0
    for range in ranges:
        total += range.size()
    total -= len(foundBeacons)
    return total

def MergeRanges(ranges: list[Range]) -> list[Range]:
    itemMerged = True

    result = None
    while itemMerged:
        itemMerged = False
        result = []

        for range in ranges:
            merged = False
            for other in result:
                if (range == other):
                    continue

                if range.intersects(other):
                    result.remove(other)
                    result.append(range.merge(other))
                    merged = True
                    itemMerged = True
                    break
        
            if not merged:
                result.append(range)
        
        ranges = result

    return result

def GetResultTwo(filename, maxVal):
    sensors: list[Sensor] = []
    beacons: list[Point] = []
    map = Bounds()

    input = common.ReadFile(filename)
    for line in input:
        match = SensorPattern.search(line)
        beaconLoc = Point(int(match.group(3)), int(match.group(4)))
        map.expand(beaconLoc)
        beacons.append(beaconLoc)

        sensorLoc = Point(int(match.group(1)), int(match.group(2)))
        map.expand(sensorLoc)
        sensor = Sensor(sensorLoc, beaconLoc)
        sensors.append(sensor)

    for sensor in sensors:
        beaconDist = sensor.beaconDist()
        #print(f"{beaconDist} - {sensor.position} {sensor.beacon}")
        map.expand(Point(sensor.position.x + beaconDist, sensor.position.y))
        map.expand(Point(sensor.position.x - beaconDist, sensor.position.y))
        map.expand(Point(sensor.position.x, sensor.position.y + beaconDist))
        map.expand(Point(sensor.position.x, sensor.position.y - beaconDist))

    result = 0
    for y in range(0, maxVal):
        print(f"{y}: {((y / maxVal) * 100):.1f}%", end='\r')
        ranges = []
        foundBeacons = []
        for sensor in sensors:
            r = sensor.intersectY(y, Range(0, maxVal))
            if r != None:
                ranges.append(r)
                ranges = MergeRanges(ranges)

            if sensor.beacon.y == y and foundBeacons.count(sensor.beacon) == 0:
                foundBeacons.append(sensor.beacon)

        # print(f"y={y}: {','.join(str(r) for r in ranges)}")
        # print(f"y={y}: {','.join(str(b) for b in foundBeacons)}")
        if len(ranges) > 1:
            ranges.sort(key=lambda r: r.min)
            print(f"y={y}: {','.join(str(r) for r in ranges)}")
            result = (ranges[0].size() * 4000000) + y
            break

        

    return result

print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST, 10)} puzzle = {GetResultOne(INPUT, 2000000)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST, 20)} puzzle = {GetResultTwo(INPUT, 4000000)}")
