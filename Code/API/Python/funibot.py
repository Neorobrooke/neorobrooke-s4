from __future__ import annotations

from math import sqrt
from traceback import print_exc


class PosVec:
    """Représente un vecteur position"""

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x};{self.y};{self.z})"

    def __add__(self, other) -> PosVec:
        try:
            return PosVec(self.x + other.x, self.y + other.y, self.z + other.z)
        except ... as e:
            print_exc()
            raise e

    def __sub__(self, other) -> PosVec:
        try:
            return PosVec(self.x - other.x, self.y - other.y, self.z - other.z)
        except ... as e:
            print_exc()
            raise e

    def __mul__(self, other) -> PosVec:
        try:
            return PosVec(self.x * other, self.y * other, self.z * other)
        except ... as e:
            print_exc()
            raise e

    def norme(self) -> float:
        try:
            return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        except ... as e:
            print_exc()
            raise e


class Poteau:
    """Représente un pôle du Funibot"""

    def __init__(self, nom, position=PosVec(0, 0, 0)) -> None:
        self.nom = nom
        self.pos = position

    def __repr__(self) -> str:
        return f"Poteau[{self.nom}]{self.pos}"


class Funibot:
    """Représente le Funibot"""

    def __init__(self, port_serie, poteaux: dict[str, Poteau]) -> None:
        pass
