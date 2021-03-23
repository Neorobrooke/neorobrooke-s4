from __future__ import annotations

from traceback import print_exc
from typing import ItemsView, Iterator, KeysView, List, ValuesView, Union, Optional

from funibot_api.funibot_json_serial import FuniErreur, FuniModeDeplacement, FuniSerial, FuniType, FuniCommException
from funibot_api.funilib import Poteau, Vecteur, Direction

class Funibot:
    """Représente le Funibot"""

    @staticmethod
    def truc():
        pass

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
