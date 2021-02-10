from __future__ import annotations

from math import sqrt, atan2
from traceback import print_exc
from numbers import Number


class PosVec:
    """Représente un vecteur position"""

    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x};{self.y};{self.z})"

    def __add__(self, other) -> PosVec:
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return PosVec(self.x + other.x, self.y + other.y, self.z + other.z)
        except ... as e:
            print_exc()
            raise e

    def __sub__(self, other) -> PosVec:
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return PosVec(self.x - other.x, self.y - other.y, self.z - other.z)
        except ... as e:
            print_exc()
            raise e

    def __mul__(self, other) -> PosVec:
        if not isinstance(other, Number):
            return NotImplemented

        try:
            return PosVec(self.x * other, self.y * other, self.z * other)
        except ... as e:
            print_exc()
            raise e

    def __rmul__(self, other) -> PosVec:
        try:
            return self.__mul__(other)
        except ... as e:
            print_exc()
            raise e

    @property
    def norme(self) -> float:
        try:
            return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        except ... as e:
            print_exc()
            raise e


class Direction:
    """Représente une direction combinée dans les trois axes"""
    def __init__(self, direction: str) -> None:
        self.axe_x, self.axe_y, self.axe_z = Direction._parse(direction)

    @staticmethod
    def _parse(direction: str) -> tuple(int):
        allowed = "+-xyz"
        if not set(direction).issubset(set(allowed)):
            raise ValueError(f"'{direction}' contient des caractères qui ne sont pas dans '{allowed}'")
        directions = {}
        for axe in 'xyz':
            if axe in direction:
                if direction[direction.find(axe) - 1] == '-':
                    directions[axe] = -1
                else:
                    directions[axe] = 1
            else:
                directions[axe] = 0

        return directions['x'], directions['y'], directions['z']

    def __repr__(self) -> str:
        return f"Direction(x:{self.axe_x}; y:{self.axe_y}; z:{self.axe_z})"

class Poteau:
    """Représente un pôle du Funibot"""

    def __init__(self, nom, position=PosVec(0, 0, 0)) -> None:
        self.nom = nom
        self.pos = position

    def __repr__(self) -> str:
        return f"Poteau[{self.nom}]{self.pos}"

    @property
    def longueur_cable(self) -> float:
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def angle_plan(self) -> float:
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def angle_chute(self) -> float:
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def courant_moteur(self) -> float:
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def couple_moteur(self) -> float:
        raise NotImplementedError("Pas encore codé dans la communication")


class Funibot:
    """Représente le Funibot"""

    def __init__(self, port_serie, poteaux: dict[str, Poteau]) -> None:
        self.port_serie = port_serie
        self.poteaux = poteaux
