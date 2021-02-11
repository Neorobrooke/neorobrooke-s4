from __future__ import annotations

from math import sqrt, atan2
from traceback import print_exc
from numbers import Number


class Vecteur:
    """Représente un vecteur position"""

    def __init__(self, x=0, y=0, z=0) -> None:
        """Initialisation du vecteur avec trois composantes x, y et z.
           Par défaut, chaque composante vaut 0."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        """Représentation du vecteur sous la forme (x;y;z)"""
        return f"({self.x};{self.y};{self.z})"

    def __add__(self, other) -> Vecteur:
        """Permet d'additionner deux vecteurs ensemble"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return Vecteur(self.x + other.x, self.y + other.y, self.z + other.z)
        except ... as e:
            print_exc()
            raise e

    def __sub__(self, other) -> Vecteur:
        """Permet de soustraire deux vecteurs l'un de l'autre"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return Vecteur(self.x - other.x, self.y - other.y, self.z - other.z)
        except ... as e:
            print_exc()
            raise e

    def __mul__(self, other) -> Vecteur:
        """Permet de multiplier un vecteur par un scalaire"""
        if not isinstance(other, Number):
            return NotImplemented

        try:
            return Vecteur(self.x * other, self.y * other, self.z * other)
        except ... as e:
            print_exc()
            raise e

    def __rmul__(self, other) -> Vecteur:
        """Permet de multiplier un vecteur par un scalaire"""
        try:
            return self.__mul__(other)
        except ... as e:
            print_exc()
            raise e

    def __truediv__(self, other) -> Vecteur:
        """Permet de diviser un vecteur par un scalaire"""
        if not isinstance(other, Number):
            return NotImplemented
        
        try:
            return Vecteur(self.x / other, self.y / other, self.z / other)
        except ... as e:
            print_exc()
            raise e

    def __floordiv__(self, other) -> Vecteur:
        """Permet de diviser (division entière) un vecteur par un scalaire"""
        if not isinstance(other, Number):
            return NotImplemented
        
        try:
            return Vecteur(self.x // other, self.y // other, self.z // other)
        except ... as e:
            print_exc()
            raise e

    def norme(self) -> float:
        """Calcule la norme du vecteur"""
        try:
            return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        except ... as e:
            print_exc()
            raise e

    def unitaire(self) -> Vecteur:
        """Retourne le vecteur unitaire ayant la même direction"""
        norme_vec = self.norme()
        return Vecteur(self.x / norme_vec, self.y / norme_vec, self.z / norme_vec)


class Direction:
    """Représente une direction combinée dans les trois axes"""
    def __init__(self, direction: str) -> None:
        """Crée une direction à partir d'une string de 'xyz+-'"""
        self.axe_x, self.axe_y, self.axe_z = Direction._parse(direction)

    @staticmethod
    def _parse(direction: str) -> tuple(int):
        """Transforme une string contenant les caractères 'xyz+-' en direction"""
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
        """Présente la direction sous la forme Direction(x:X; y:Y; z:Z).
           Ici, X, Y et Z sont soit -1, 0 ou 1."""
        return f"Direction(x:{self.axe_x}; y:{self.axe_y}; z:{self.axe_z})"

    def vecteur(self):
        """Retourne un Vecteur correspondant à la direction"""
        return Vecteur(self.axe_x, self.axe_y, self.axe_z)


class Poteau:
    """Représente un pôle du Funibot"""

    def __init__(self, nom, position=Vecteur(0, 0, 0)) -> None:
        self.nom = nom
        self.pos = position

    def __repr__(self) -> str:
        return f"Poteau[{self.nom}]{self.pos}"

    @property
    def longueur_cable(self) -> float:
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
