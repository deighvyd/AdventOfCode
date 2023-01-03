from __future__ import annotations

class Vector3:
    Zero: Vector3
    One: Vector3
    X: Vector3
    Y: Vector3
    Z: Vector3
    INF: Vector3

    def __init__(self, x, y, z) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> Vector3:
        return Vector3(-self.x, -self.y, -self.z)

    def __hash__(self) -> int:
        return hash(str(self))

    def copy(self) -> Vector3:
        return Vector3(self.x, self.y, self.z)

Vector3.Zero = Vector3(0, 0, 0)
Vector3.One = Vector3(1, 1, 1)
Vector3.X = Vector3(1, 0, 0)
Vector3.Y = Vector3(0, 1, 0)
Vector3.Z = Vector3(0, 0, 1)
Vector3.INF = Vector3(float('inf'), float('inf'), float('inf'))

class Bounds3:
    def __init__(self) -> None:
        self.min = Vector3.INF.copy()
        self.max = -Vector3.INF.copy()
        self.bounds = [-1, -1, -1]

    def area(self) -> int:
        return self.bounds[0] * self.bounds[1] * self.bounds[2]

    def expand(self, point: Vector3) -> None:
        self.min.x = min(point.x, self.min.x)
        self.min.y = min(point.y, self.min.y)
        self.min.z = min(point.z, self.min.z)

        self.max.x = max(point.x, self.max.x)
        self.max.y = max(point.y, self.max.y)
        self.max.z = max(point.z, self.max.z)

        self.bounds = [self.max.x - self.min.x + 1, self.max.y - self.min.y + 1, self.max.z - self.min.z + 1]

    def contains(self, point: Vector3) -> bool:
        if self.min.x <= point.x <= self.max.x and self.min.y <= point.y <= self.max.y and self.min.z <= point.z <= self.max.z:
           return True
        
        return False

    def forEach(self, visitor, data) -> None:
        if visitor == None:
            return

        for i in range(0, self.bounds[0]):
            for j in range(0, self.bounds[1]):
                for k in range(0, self.bounds[2]):
                    loc = Vector3(self.min.x + i, self.min.y + j, self.min.z + k)
                    visitor(i, j, k, loc, data)