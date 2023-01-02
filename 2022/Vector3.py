from __future__ import annotations

class Vector3:
    Zero: Vector3
    One: Vector3
    X: Vector3
    Y: Vector3
    Z: Vector3

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

    def clone(self) -> Vector3:
        return Vector3(self.x, self.y)

Vector3.Zero = Vector3(0, 0, 0)
Vector3.One = Vector3(1, 1, 1)
Vector3.X = Vector3(1, 0, 0)
Vector3.Y = Vector3(0, 1, 0)
Vector3.Z = Vector3(0, 0, 1)