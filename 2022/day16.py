from __future__ import annotations

import common
import re

from itertools import combinations

DAY = 16
INPUT=f"day{DAY}.input"
INPUT_TEST=f"{INPUT}.test"

class Valve:
    __InputPattern = re.compile(r"Valve (..) has flow rate=(.*); tunnels? leads? to valves? (.*)")
    def __init__(self, id: str, rate: int, tunnels: list[str]) -> None:
        self.id = id
        self.rate = rate
        self.tunnels = tunnels

    def __str__(self) -> str:   
        return f"ID: {self.id} FR={self.rate} TNLS={','.join(self.tunnels)}"

    @classmethod
    def Read(cls, input: str) -> Valve:
        match = cls.__InputPattern.search(input)
        if match != None:
            return Valve(match.group(1), int(match.group(2)), match.group(3).split(', '))

        return None

class Search:
    MaxTime = 30
    def __init__(self, valveId: str, time: int, rate: int, total: int, open: list[str] = None, visited: list[str] = None) -> None:
        self.valveId = valveId
        self.time = time
        self.rate = rate
        self.total = total
        self.open = []
        if open != None:
            for v in open:
                self.open.append(v)
        self.visited = []
        if visited != None:
            for v in visited:
                self.visited.append(v)

    def __str__(self) -> str:
        return f"t={self.time} r={self.rate} p={self.total} o=[{','.join(self.open)}]"

    def simulateTime(self, time: int) -> None:
        self.total += (self.rate * time)
        self.time += time

    def simulateToEnd(self) -> None:
        self.simulateTime(Search.MaxTime - self.time)

    def clone(self) -> Search:
        return Search(self.valveId, self.time, self.rate, self.total, self.open, self.visited)

def FindPath(start: str, end: str, valves: list[Valve]) -> list[str]:
    class node:
        def __init__(self, valve: str, parent: node = None) -> None:
            self.valve = valve
            self.g = 0
            self.h = 1
            self.parent = parent
        
        def __eq__(self, __o: node) -> bool:
            if __o == None:
                return False

            return self.valve == __o.valve

    open = [node(end)]
    closed = []
    pathEnd = None
    while len(open) > 0 and pathEnd == None:
        curr = open.pop()
        closed.append(curr.valve)
        for tunnel in valves[curr.valve].tunnels:
            if tunnel in closed:
                continue

            new = node(tunnel, curr)
            if tunnel == start:
                pathEnd = new
                break
            
            new.g = curr.g + 1
            for n in open:
                if n.valve == new.valve and new.g < n.g:
                    n.g = new.g
            else:
                open.append(new)
        open.sort(key=lambda n: (n.g + n.h), reverse=True)
    
    path = []
    while pathEnd != None:
        path.append(pathEnd.valve)
        pathEnd = pathEnd.parent
    return path

def SearchValves(valves, pathSizes, nodes):
    results = {}
    
    searches = []
    for node in nodes:
        path = FindPath('AA', node.id, valves)
        searches.append(Search(node.id, len(path) - 1, 0, 0))

    while len(searches) > 0:
        search = searches.pop()
        valve = valves[search.valveId]

        # open the valve
        search.simulateTime(1)
        search.rate += valve.rate
        search.open.append(valve.id)
        if len(search.open) == len(nodes):
            search.simulateToEnd()
            results[search.total] = search
            continue

        for node in nodes:
            if node.id in search.open:
                continue
            
            pathSize = pathSizes[f"{search.valveId}->{node.id}"]
            if search.time + pathSize > Search.MaxTime:
                search.simulateToEnd()
                results[search.total] = search
                continue

            newSearch = search.clone()
            newSearch.simulateTime(pathSize)
            newSearch.valveId = node.id
            searches.append(newSearch)

    return results

def GetResultOne(filename):
    Search.MaxTime = 30
    
    valves = {}
    nodes = []
    for line in common.ReadFile(filename):
        valve = Valve.Read(line)
        valves[valve.id] = valve
        if valve.rate > 0:
            nodes.append(valve)

    pathSizes = {}
    for i in range(0, len(nodes)):
        for j in range (i + 1, len(nodes)):
            path = FindPath(nodes[i].id, nodes[j].id, valves)

            key = f"{nodes[i].id}->{nodes[j].id}"
            pathSizes[key] = len(path) - 1

            key = f"{nodes[j].id}->{nodes[i].id}"
            pathSizes[key] = len(path) - 1

    # for key in paths.keys():
    #     print(f"{key} = {'->'.join(paths[key])}")
    results = SearchValves(valves, pathSizes, nodes)
    
    return max(results.keys())

def GetResultTwo(filename):
    Search.MaxTime = 26
    
    valves = {}
    nodes = []
    for line in common.ReadFile(filename):
        valve = Valve.Read(line)
        valves[valve.id] = valve
        if valve.rate > 0:
            nodes.append(valve)

    pathSizes = {}
    for i in range(0, len(nodes)):
        for j in range (i + 1, len(nodes)):
            path = FindPath(nodes[i].id, nodes[j].id, valves)

            key = f"{nodes[i].id}->{nodes[j].id}"
            pathSizes[key] = len(path) - 1

            key = f"{nodes[j].id}->{nodes[i].id}"
            pathSizes[key] = len(path) - 1

    scores = {}

    # generate sets of 3
    for combination in combinations(nodes, int(len(nodes) / 2)):
        key = ','.join(n.id for n in combination)

        results = SearchValves(valves, pathSizes, combination)
        scores[key] = max(results.keys())

        compliment = list(set(nodes) - set(combination))
        results = SearchValves(valves, pathSizes, compliment)
        scores[key] += max(results.keys())    

    bestScore = 0
    for key in scores.keys():
        if scores[key] > bestScore:
            bestScore = scores[key]

    return bestScore

#print(f"Day {DAY}.1: test = {GetResultOne(INPUT_TEST)} puzzle = {GetResultOne(INPUT)}")
print(f"Day {DAY}.2: test = {GetResultTwo(INPUT_TEST)} puzzle = {GetResultTwo(INPUT)}")
