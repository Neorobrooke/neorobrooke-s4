from __future__ import annotations

from math import sqrt
from traceback import print_exc
from numbers import Number
from typing import ContextManager, ItemsView, Iterator, KeysView, ValuesView, Union
from contextlib import contextmanager


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

    def __iadd__(self, other) -> Vecteur:
        """Permet d'ajouter un autre vecteur à celui-ci"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        bckup = (self.x, self.y, self.z)
        try:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        except ... as e:
            print_exc()
            self.x = bckup(0)
            self.y = bckup(1)
            self.z = bckup(2)
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

    def __isub__(self, other) -> Vecteur:
        """Permet de soustraire un autre vecteur à celui-ci"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        bckup = (self.x, self.y, self.z)
        try:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        except ... as e:
            print_exc()
            self.x = bckup(0)
            self.y = bckup(1)
            self.z = bckup(2)
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

    def __imul__(self, other) -> Vecteur:
        """Permet de multiplier ce vecteur par un scalaire"""

        bckup = (self.x, self.y, self.z)
        try:
            self.x *= other
            self.y *= other
            self.z *= other
        except ... as e:
            print_exc()
            self.x = bckup(0)
            self.y = bckup(1)
            self.z = bckup(2)
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

    def __itruediv__(self, other) -> Vecteur:
        """Permet de diviser ce vecteur par un scalaire"""

        bckup = (self.x, self.y, self.z)
        try:
            self.x /= other
            self.y /= other
            self.z /= other
        except ... as e:
            print_exc()
            self.x = bckup(0)
            self.y = bckup(1)
            self.z = bckup(2)
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

    def __ifloordiv__(self, other) -> Vecteur:
        """Permet de diviser (division entière) ce vecteur par un scalaire"""

        bckup = (self.x, self.y, self.z)
        try:
            self.x //= other
            self.y //= other
            self.z //= other
        except ... as e:
            print_exc()
            self.x = bckup(0)
            self.y = bckup(1)
            self.z = bckup(2)
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

    def vers_tuple(self) -> tuple(float, float, float):
        return (self.x, self.y, self.z)


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
            raise ValueError(
                f"'{direction}' contient des caractères qui ne sont pas dans '{allowed}'")
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

    def __init__(self, nom, position: Vecteur = Vecteur(0, 0, 0)) -> None:
        """Initialise un Poteau pour le Funibot.
           'nom=' est l'identifiant du Poteau
           'position=' est un Vecteur donnant les coordonnées du Poteau.
           Par défaut, position = (0;0;0).
           Nécessite une communication série.
        """
        self.nom = nom
        self.pos = position

    def __repr__(self) -> str:
        """Représente le Poteau sous la forme Poteau[nom](x;y;z)"""
        return f"Poteau[{self.nom}]{self.pos}"

    @property
    def longueur_cable(self) -> float:
        """Donne la longueur actuelle du câble associé à ce poteau
           Nécessite une communication série.
        """
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def courant_moteur(self) -> float:
        """Donne le courant actuel du moteur associé à ce poteau
           Nécessite une communication série.
        """
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def couple_moteur(self) -> float:
        """Donne le couple actuel du moteur associé à ce poteau
           Nécessite une communication série.
        """
        raise NotImplementedError("Pas encore codé dans la communication")


class Funibot:
    """Représente le Funibot"""

    def __init__(self, port_serie, poteaux: list[Poteau]) -> None:
        self.port_serie = port_serie
        self.poteaux = Funibot._poteaux_liste_a_dict(poteaux)

    @property
    def pos(self) -> float:
        """Retourne la position actuelle du Funibot.
           Nécessite une communication série.
        """
        raise NotImplementedError("Pas encore dans la communication")

    @pos.setter
    def pos(self, position: Vecteur) -> None:
        """Déplace le Funibot à la posision vectorielle demandée.
           Nécessite une communication série.
        """
        raise NotImplementedError("Pas encore dans la communication")

    def __getitem__(self, nom: str) -> Poteau:
        """Retourne le poteau ayant le nom demandé"""
        return self.poteaux[nom]

    def keys(self) -> ValuesView:
        """Retourne une vue sur les clés du dict des poteaux"""
        return self.poteaux.keys()

    def values(self) -> KeysView:
        """Retourne une vue sur les valeurs du dict des poteaux"""
        return self.poteaux.values()

    def items(self) -> ItemsView:
        """Retourne une vue sur les items du dict des poteaux"""
        return self.poteaux.items()

    def __iter__(self) -> Iterator:
        """Retourne un générateur pour itérer sur les poteaux du funibot"""
        return (key for key in self.poteaux.values())

    def __repr__(self) -> str:
        """Représente le Funibot sous la forme Funibot[port_serie](poteaux)"""
        return f"Funibot[{self.port_serie}]({self.poteaux.values()})"

    @contextmanager
    def deplacer(self, direction: Union[Direction, Vecteur, str], distance: float=None) -> Union[float, None]:
        """Déplace le Funibot dans la direction indiquée par 'direction'.
           Utilisable comme un contextmanager (avec 'with')
           Si 'distance' n'est pas None, arrête après avoir parcouru 'distance'.
           Sinon, arrête à la fin du 'with'.
           Retourne la durée prévue du déplacement, ou None si aucune distance n'est précisée.
           Nécessite une communication série.
        """

        if isinstance(direction, str):
            direction = Direction(direction=direction)

        if isinstance(direction, Direction):
            direction = direction.vecteur()

        # Envoyer un commencer
        try:
            yield (None if distance is None else 0.0)
        except KeyboardInterrupt:
            pass
        
        # Attendre fin du déplacement si distance non-nulle
        if distance is not None:
            try:
                # Attendre
                pass
            except KeyboardInterrupt:
                pass
        else:
            # Envoyer un stop
            pass

        return None

    @staticmethod
    def _poteaux_liste_a_dict(poteaux: list[Poteau]) -> dict[str, Poteau]:
        """Crée un dict avec la liste de poteaux, en utilisant le nom comme clé"""
        poteaux_dict = {}
        for poteau in poteaux:
            poteaux_dict[poteau.nom] = poteau
        return poteaux_dict
