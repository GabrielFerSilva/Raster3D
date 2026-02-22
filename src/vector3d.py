import numpy as np

class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3D':
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> 'Vector3D':
        return self.__class__(self.x / scalar, self.y / scalar, self.z / scalar)

    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self) -> 'Vector3D':
        mag = self.length()
        if mag == 0:
            raise ValueError("Cannot normalize a zero-length vector")
        return self.__class__(self.x / mag, self.y / mag, self.z / mag)

    def __matmul__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)

    def __array__(self, dtype=None):
        return np.array([self.x, self.y, self.z], dtype=dtype)

    def __rmatmul__(self, other):
        if isinstance(other, (np.matrix, np.ndarray)):
            # Garantimos que a matriz seja tratada como um array para indexação
            m = np.asarray(other)
            
            # Cálculo do produto escalar de cada linha da matriz pelo vetor
            new_x = m[0, 0] * self.x + m[0, 1] * self.y + m[0, 2] * self.z
            new_y = m[1, 0] * self.x + m[1, 1] * self.y + m[1, 2] * self.z
            new_z = m[2, 0] * self.x + m[2, 1] * self.y + m[2, 2] * self.z
            
            return Vector3D(new_x, new_y, new_z)

    def __str__(self) -> str:
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __neg__(self) -> 'Vector3D':
        return self.__class__(-self.x, -self.y, -self.z)