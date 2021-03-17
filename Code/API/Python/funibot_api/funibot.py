from __future__ import annotations

from math import sqrt
from traceback import print_exc
from numbers import Real
from string import digits
from typing import Dict, ItemsView, Iterator, KeysView, List, ValuesView, Union, Tuple, Optional

from funibot_api.funibot_json_serial import FuniErreur, FuniModeCalibration, FuniModeDeplacement, FuniSerial, FuniType, FuniCommException


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


class ChangerNormeVecteurNulErreur(Exception):
    pass


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
            raise ChangerNormeVecteurNulErreur(
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

        allowed = f"+-xyz{digits}"

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
            if direction[index] in f'+-{digits}':
                val = f"{val}{direction[index]}"
                if not check_signe and direction[index] in '+-':
                    raise ValueError(
                        "Double signe ou signe ailleurs qu'au début")
            check_signe = False

            if direction[index] in axes:
                if direction[index] in directions:
                    raise ValueError(
                        f"L'axe {direction[index]} apparaît plusieurs fois")
                if val in '+-' or val == '':
                    val = f"{val}1"
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
        self.serial.pot(type=FuniType.SET, id=self.id,
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

    def repr_moteur(self) -> str:
        """Représente le Moteur associé au Poteau sous la forme Moteur[id:nom] -> I: (courant) T: <couple>"""
        return f"Moteur[{self.id}:{self.nom}] -> I: ({self.courant_moteur}) T: <{self.couple_moteur}>"

    def repr_complet(self) -> str:
        """Représente le Poteau sous la forme Poteau[id:nom](px;py;pz)(ax;ay;az) -> L: {longueur} I: (courant) T: <couple>
           Le vecteur (px;py;pz) représente la position du poteau
           Le vecteur (ax;ay;az) représente la position de l'attache sur la nacelle par rapport au TCP du robot
           (Le TCP est le Tool Center Point)
        """
        return f"{self.__repr__()} -> L: {{{self.longueur_cable}}} I: ({self.courant_moteur}) T: <{self.couple_moteur}>"

    @property
    def longueur_cable(self) -> Optional[Union[float, str]]:
        """Donne la longueur actuelle du câble associé à ce poteau
           Nécessite une communication série.
        """
        if self.id is None or self.serial is None:
            raise JamaisInitialise(self, "longueur_cable")
        try:
            return self.serial.cal(
                FuniType.GET, FuniModeCalibration.CABLE, self.id, None)
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
                FuniType.SET, FuniModeCalibration.CABLE, self.id, longueur)
        except Exception:
            print_exc()
            raise

    @property
    def courant_moteur(self) -> float:
        """Donne le courant actuel du moteur associé à ce poteau
           Nécessite une communication série.
        """
        if self.id is None or self.serial is None:
            raise JamaisInitialise(self, "courant_moteur")
        raise NotImplementedError("Pas encore codé dans la communication")

    @property
    def couple_moteur(self) -> float:
        """Donne le couple actuel du moteur associé à ce poteau
           Nécessite une communication série.
        """
        if self.id is None or self.serial is None:
            raise JamaisInitialise(self, "couple_moteur")
        raise NotImplementedError("Pas encore codé dans la communication")


class Funibot:
    """Représente le Funibot"""

    def __init__(self, serial: FuniSerial, poteaux: list[Poteau]) -> None:
        self.serial = serial
        self.poteaux = Funibot._poteaux_liste_a_dict(poteaux)
        self._initialiser_poteaux()

    @property
    def pos(self) -> Vecteur:
        """Retourne la position actuelle du Funibot.
           Nécessite une communication série.
        """
        valeur = self.serial.pos(FuniType.GET)
        if isinstance(valeur, str):
            raise FuniCommException(valeur)
        return Vecteur(*valeur)

    @pos.setter
    def pos(self, position: Vecteur) -> None:
        """Déplace le Funibot à la posision vectorielle demandée.
           Nécessite une communication série.
        """
        valeur = self.serial.pos(FuniType.SET, position.vers_tuple())
        if isinstance(valeur, str):
            raise FuniCommException(valeur)
        return

    def __getitem__(self, nom: str) -> Poteau:
        """Retourne le poteau ayant le nom demandé"""
        return self.poteaux[nom]

    def keys(self) -> KeysView:
        """Retourne une vue sur les clés du dict des poteaux"""
        return self.poteaux.keys()

    def values(self) -> ValuesView[Poteau]:
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
        return f"Funibot[{self.serial}]({list(self.poteaux.values())})"

    def deplacer(self, direction: Union[Direction, Vecteur, str], distance: float = None):
        """Déplace le Funibot dans la direction indiquée par 'direction'.
           Si 'distance' n'est pas None, arrête après avoir parcouru 'distance'.
           Si 'distance' est la valeur spéciale 0, arrête après avoir parcouru la distance correspondant à la norme du vecteur
           Sinon, arrête avec un appel à 'stop'
           Nécessite une communication série.
        """
        if isinstance(direction, str):
            direction = Direction(direction=direction)

        if isinstance(direction, Direction):
            direction = direction.vecteur()

        mode = FuniModeDeplacement.START if distance is None else FuniModeDeplacement.DISTANCE

        if distance is not None and distance != 0:
            direction = direction.unitaire() * distance

        self.serial.dep(type=FuniType.SET, mode=mode,
                        direction=direction.vers_tuple())
        return None

    def stop(self) -> None:
        self.serial.dep(type=FuniType.SET, mode=FuniModeDeplacement.STOP)
        return None

    def erreur(self) -> Optional[List[FuniErreur]]:
        try:
            erreurs = self.serial.err(FuniType.GET)
            return erreurs
        except Exception:
            print_exc()
            return None

    @staticmethod
    def _poteaux_liste_a_dict(poteaux: list[Poteau]) -> dict[str, Poteau]:
        """Crée un dict avec la liste de poteaux, en utilisant le nom comme clé"""
        poteaux_dict = {}
        for poteau in poteaux:
            poteaux_dict[poteau.nom] = poteau
        return poteaux_dict

    def _initialiser_poteaux(self):
        """Donne un ID et assigne l'objet serial à chaque poteau"""
        self.poteaux_id: List[Poteau] = []
        for poteau in self.poteaux.values():
            try:
                poteau.init_poteau(
                    id=len(self.poteaux_id), comm_serie=self.serial)
            except Exception:
                print_exc()
                raise
            self.poteaux_id.append(poteau)
