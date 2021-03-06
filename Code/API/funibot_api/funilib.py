from __future__ import annotations

from enum import Enum, auto
from math import sqrt
from traceback import print_exc
from numbers import Real
from string import digits
from typing import Union, Tuple, Optional, List

from funibot_api.funiserial import FuniErreur, eFuniModeCalibration, eFuniModeDeplacement, FuniSerial, eFuniType, FuniCommException


class JamaisInitialise(Exception):
    """Exception pour un poteau jamais initialisé par un Funibot qui essaie de communiquer en série"""

    def __init__(self, poteau: Poteau = None, message: str = None):
        if poteau is None:
            n_poteau: Union[Poteau, str] = "Ce Poteau"
        else:
            n_poteau: Union[Poteau, str] = poteau

        self.message = f"{n_poteau} n'est pas initialisé dans un Funibot et n'a pas de port série"
        if message is not None:
            self.message = f"{self.message} -> Impossible d'accéder à '{message}'"

        super().__init__(self.message)


class ErreurChangerNormeVecteurNul(Exception):
    """Levée lorsqu'on essaie de changer la norme du vecteur nul"""
    pass


class eRetourAttendre(Enum):
    """Représente les possibilités de retour lors de l'attente.
       OK -> Attente réalisée avec succès
       ATTENTE_INVALIDE -> Il n'était pas nécessaire d'attendre
       ARRET_INVALIDE -> L'arrêt a été causé par une erreur ou l'atteinte de la limite de la zone de travail
       ERREUR_COMM -> Erreur de communication
    """
    OK = auto()
    ATTENTE_INVALIDE = auto()
    ARRET_INVALIDE = auto()
    ERREUR_COMM = auto()


class sEntreeAttendre:
    def __init__(self, nom_methode: str, retour_attendre: eRetourAttendre) -> None:
        self.nom_methode = nom_methode
        self.retour_attendre = retour_attendre


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

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __add__(self, other) -> Vecteur:
        """Permet d'additionner deux vecteurs ensemble"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return Vecteur(self.x + other.x, self.y + other.y, self.z + other.z)
        except Exception:
            print_exc()
            raise

    def __iadd__(self, other: Vecteur) -> Vecteur:
        """Permet d'ajouter un autre vecteur à celui-ci"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        bckup = (self.x, self.y, self.z)
        try:
            self.x += other.x
            self.y += other.y
            self.z += other.z
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

        return self

    def __sub__(self, other) -> Vecteur:
        """Permet de soustraire deux vecteurs l'un de l'autre"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        try:
            return Vecteur(self.x - other.x, self.y - other.y, self.z - other.z)
        except Exception:
            print_exc()
            raise

    def __isub__(self, other) -> Vecteur:
        """Permet de soustraire un autre vecteur à celui-ci"""
        if not isinstance(other, self.__class__):
            return NotImplemented

        bckup = (self.x, self.y, self.z)
        try:
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

        return self

    def __mul__(self, other) -> Vecteur:
        """Permet de multiplier un vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented

        try:
            return Vecteur(self.x * other, self.y * other, self.z * other)
        except Exception:
            print_exc()
            raise

    def __rmul__(self, other) -> Vecteur:
        """Permet de multiplier un vecteur par un scalaire"""
        return self * other

    def __imul__(self, other) -> Vecteur:
        """Permet de multiplier ce vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented  # type: ignore

        bckup = (self.x, self.y, self.z)
        try:
            self.x *= other
            self.y *= other
            self.z *= other
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

        return self

    def __truediv__(self, other) -> Vecteur:
        """Permet de diviser un vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented

        try:
            return Vecteur(self.x / other, self.y / other, self.z / other)
        except Exception:
            print_exc()
            raise

    def __itruediv__(self, other) -> Vecteur:
        """Permet de diviser ce vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented  # type: ignore

        bckup = (self.x, self.y, self.z)
        try:
            self.x /= other
            self.y /= other
            self.z /= other
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

        return self

    def __floordiv__(self, other) -> Vecteur:
        """Permet de diviser (division entière) un vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented

        try:
            return Vecteur(self.x // other, self.y // other, self.z // other)
        except Exception:
            print_exc()
            raise

    def __ifloordiv__(self, other) -> Vecteur:
        """Permet de diviser (division entière) ce vecteur par un scalaire"""
        if not isinstance(other, Real):
            return NotImplemented  # type: ignore

        bckup = (self.x, self.y, self.z)
        try:
            self.x //= other
            self.y //= other
            self.z //= other
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

        return self

    @property
    def norme(self) -> float:
        """Calcule la norme du vecteur"""
        try:
            return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        except Exception:
            print_exc()
            raise

    @norme.setter
    def norme(self, longueur) -> None:
        """Change la norme du vecteur"""
        norme = self.norme
        if norme == 0:
            raise ErreurChangerNormeVecteurNul(
                "Impossible d'assigner une norme au vecteur nul, car il n'as pas d'orientation")

        bckup = (self.x, self.y, self.z)
        try:
            self.x *= longueur/norme
            self.y *= longueur/norme
            self.z *= longueur/norme
        except Exception:
            print_exc()
            self.x = bckup[0]
            self.y = bckup[1]
            self.z = bckup[2]
            raise

    def unitaire(self) -> Vecteur:
        """Retourne le vecteur unitaire ayant la même direction"""
        norme_vec = self.norme
        try:
            return Vecteur(self.x / norme_vec, self.y / norme_vec, self.z / norme_vec)
        except ZeroDivisionError:
            return Vecteur(0, 0, 0)

    def vers_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


class Direction:
    """Représente une direction combinée dans les trois axes"""

    def __init__(self, direction: str) -> None:
        """Crée une direction à partir d'une string de 'xyz+-'"""
        self.axe_x, self.axe_y, self.axe_z = Direction._parse(direction)

    @staticmethod
    def _parse(direction: str) -> Tuple[int, int, int]:
        """Transforme une string contenant les caractères 'xyz+-' en direction"""

        allowed = f".,+-xyz{digits}"

        if not set(direction).issubset(set(allowed)):
            raise ValueError(
                f"'{direction}' contient des caractères qui ne sont pas dans '{allowed}'")

        if direction == '0':
            return (0, 0, 0)

        directions = {}

        val = ''
        axes = 'xyz'
        check_signe = True
        for index in range(len(direction)):
            if direction[index] in f'.,+-{digits}':
                if direction[index] == ',':
                    val = f"{val}{'.'}"
                else:
                    val = f"{val}{direction[index]}"
                if not check_signe and direction[index] in '+-':
                    raise ValueError(
                        "Double signe ou signe ailleurs qu'au début")
            check_signe = False

            if direction[index] in axes:
                if direction[index] in directions:
                    raise ValueError(
                        f"L'axe <{direction[index]}> apparaît plusieurs fois")
                if val in '+-' or val == '':
                    val = f"{val}1"
                try:
                    directions[direction[index]] = int(val)
                except ValueError:
                    directions[direction[index]] = float(val)
                check_signe = True
                val = ''

        pas_dans_direction = []
        for axe in axes:
            try:
                directions[axe]
            except KeyError:
                pas_dans_direction.append(axe)
                directions[axe] = 0

        if len(pas_dans_direction) == len(axes):
            raise ValueError("L'argument ne contient aucun axe")

        return (directions['x'], directions['y'], directions['z'])

    def __repr__(self) -> str:
        """Présente la direction sous la forme Direction(x:X; y:Y; z:Z).
           Ici, X, Y et Z sont soit -1, 0 ou 1."""
        return f"Direction(x:{self.axe_x}; y:{self.axe_y}; z:{self.axe_z})"

    def vecteur(self):
        """Retourne un Vecteur correspondant à la direction"""
        return Vecteur(self.axe_x, self.axe_y, self.axe_z)


class Poteau:
    """Représente un pôle du Funibot"""

    def __init__(self, nom: str, position_pole: Vecteur = Vecteur(0, 0, 0),
                 position_accroche: Vecteur = Vecteur(0, 0, 0)) -> None:
        """Initialise un Poteau pour le Funibot.
           'nom=' est l'identifiant du Poteau
           'position=' est un Vecteur donnant les coordonnées du Poteau.
           Par défaut, position = (0;0;0).
        """
        self.nom = nom
        self.pos_pole = position_pole
        self.pos_acccroche = position_accroche
        self.pos_resultante = position_pole - position_accroche
        self.id = -1
        self.serial = None

    def init_poteau(self, id: int, comm_serie: FuniSerial):
        """Initialise le poteau à l'intérieur du Funibot
           Nécessite une communication série.
        """
        self.id = id
        self.serial = comm_serie
        self.serial.pot(type=eFuniType.SET, id=self.id,
                        position=self.pos_resultante.vers_tuple())

    def __repr__(self) -> str:
        """Représente le Poteau sous la forme Poteau[id:nom](px;py;pz)(ax;ay;az)
           Le vecteur (px;py;pz) représente la position du poteau
           Le vecteur (ax;ay;az) représente la position de l'attache sur la nacelle par rapport au TCP du robot
           (Le TCP est le Tool Center Point)
        """
        return f"Poteau[{self.id}:{self.nom}]{self.pos_pole}{self.pos_acccroche}"

    def repr_cable(self) -> str:
        """Représente le Câble associé au Poteau sous la forme Câble[id:nom] -> longueur"""
        return f"Câble[{self.id}:{self.nom}] -> {self.longueur_cable}"

    def repr_complet(self) -> str:
        """Représente le Poteau sous la forme Poteau[id:nom](px;py;pz)(ax;ay;az) -> L: {longueur} I: (courant) T: <couple>
           Le vecteur (px;py;pz) représente la position du poteau
           Le vecteur (ax;ay;az) représente la position de l'attache sur la nacelle par rapport au TCP du robot
           (Le TCP est le Tool Center Point)
        """
        return f"{self.__repr__()} -> Câble: {{{self.longueur_cable}}}"

    @property
    def longueur_cable(self) -> Optional[Union[float, str]]:
        """Donne la longueur actuelle du câble associé à ce poteau
           Nécessite une communication série.
        """
        if self.id is None or self.serial is None:
            raise JamaisInitialise(self, "longueur_cable")
        try:
            return self.serial.cal(
                eFuniType.GET, eFuniModeCalibration.CABLE, self.id, None)
        except Exception:
            print_exc()
            raise

    @longueur_cable.setter
    def longueur_cable(self, longueur: float) -> None:
        """Initialise la longueur du cable pour ce poteau
           Nécessite une communication série.
        """
        if self.id is None or self.serial is None:
            raise JamaisInitialise(self, "longueur_cable.setter")
        try:
            self.serial.cal(
                eFuniType.SET, eFuniModeCalibration.CABLE, self.id, longueur)
        except Exception:
            print_exc()
            raise
