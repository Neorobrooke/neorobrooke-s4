from __future__ import annotations
from os import sep

from traceback import print_exc
from typing import ItemsView, Iterator, KeysView, List, ValuesView, Union, Optional
from pathlib import Path

from funibot_api.funiserial import FuniErreur, FuniModeCalibration, FuniModeDeplacement, FuniSerial, FuniType, FuniCommException
from funibot_api.funiconfig import FuniConfig
from funibot_api.funilib import Poteau, Vecteur, Direction
from funibot_api.funipersistance import FuniPersistance, ErreurDonneesIncompatibles


class Funibot:
    """Représente le Funibot"""

    def __init__(self, serial: FuniSerial, config: FuniConfig) -> None:
        self.serial = serial
        self.poteaux = Funibot._poteaux_liste_a_dict(config.liste_poteaux)
        self._initialiser_poteaux()
        self._sol = config.sol
        self.sol = config.sol
        
        self._initialiser_persistance(
            fichier=config.persistance,
            auto_persistance=config.auto_persistance,
            auto_calibration=config.auto_calibration)
        
        self.config = config

        if self.auto_calibration:
            try:
                self.calibrer()
            except ErreurDonneesIncompatibles as e:
                raise ErreurDonneesIncompatibles(f"Erreur de calibration automatique: {e}")

    def __del__(self):
        if self.auto_persistance:
            try:
                self.enregister_calibration()
            except ErreurDonneesIncompatibles as e:
                raise ErreurDonneesIncompatibles(f"Erreur de persistance automatique: {e}")


    @property
    def pos(self) -> Optional[Vecteur]:
        """Retourne la position actuelle du Funibot.
           Nécessite une communication série.
        """
        valeur = self.serial.pos(FuniType.GET)
        if valeur is None:
            return None
        return Vecteur(*valeur)

    @pos.setter
    def pos(self, position: Vecteur) -> None:
        """Déplace le Funibot à la posision vectorielle demandée.
           Nécessite une communication série.
        """
        self.serial.pos(FuniType.SET, position.vers_tuple())

    @property
    def sol(self) -> Optional[float]:
        # """Retourne la position du sol.
        #    Nécessite une communication série.
        # """
        """Retourne la position du sol."""
        # return self.serial.cal(FuniType.GET, FuniModeCalibration.SOL)
        return self._sol

    @sol.setter
    def sol(self, position: Optional[float]) -> None:
        """Change la position du sol.
           Nécessite une communication série.
        """
        valeur = self.serial.cal(
            FuniType.SET, FuniModeCalibration.SOL, longueur=position)
        if valeur is not None:
            self._sol = valeur

    def __getitem__(self, nom: str) -> Poteau:
        """Retourne le poteau ayant le nom demandé"""
        return self.poteaux[nom]

    def keys(self) -> KeysView[str]:
        """Retourne une vue sur les clés du dict des poteaux"""
        return self.poteaux.keys()

    def values(self) -> ValuesView[Poteau]:
        """Retourne une vue sur les valeurs du dict des poteaux"""
        return self.poteaux.values()

    def items(self) -> ItemsView[str, Poteau]:
        """Retourne une vue sur les items du dict des poteaux"""
        return self.poteaux.items()

    def __iter__(self) -> Iterator[Poteau]:
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
            direction.norme = distance

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

    def repr_sol(self):
        return f"Sol -> {self.sol}"

    def enregister_calibration(self) -> None:
        try:
            self.persistance.enregistrer(
                self._poteaux_config(), self._longueur_cables())
        except AttributeError:
            print(
                "Impossible d'enregistrer la calibration: aucun fichier de persistance valide fourni.")
        except ErreurDonneesIncompatibles as e:
            print("Impossible d'enregistrer", end=': ')
            print(e)

    def calibrer(self):
        try:
            for cle, longueur in self.persistance.calibrer(self._poteaux_config()).items():
                self.poteaux[cle].longueur_cable = longueur
        except AttributeError:
            print("Impossible de calibrer: aucun fichier de persistance valide fourni.")

    def _poteaux_config(self) -> List[dict]:
        poteaux = []
        for poteau in self.poteaux.values():
            pole = {"x": poteau.pos_pole.x,
                    "y": poteau.pos_pole.y, "z": poteau.pos_pole.z}
            accroche = {"x": poteau.pos_acccroche.x,
                        "y": poteau.pos_acccroche.y, "z": poteau.pos_acccroche.z}
            dict_poteau = {poteau.nom: {"poles": pole, "accroches": accroche}}
            poteaux.append(dict_poteau)
        return poteaux

    def _longueur_cables(self) -> List[float]:
        longueurs = []
        for poteau in self.poteaux.values():
            longueurs.append(poteau.longueur_cable)
        return longueurs

    def _initialiser_poteaux(self):
        """Donne un ID et assigne l'objet serial à chaque poteau"""
        self.poteaux_id: List[Poteau] = []
        for poteau in self.poteaux.values():
            poteau.init_poteau(
                id=len(self.poteaux_id), comm_serie=self.serial)
            self.poteaux_id.append(poteau)

    def _initialiser_persistance(self, fichier: Optional[Path],
                                 auto_calibration: bool,
                                 auto_persistance: bool):
        if fichier is None:
            self.persistance = None
            self.auto_persistance = False
            self.auto_calibration = False
        else:
            self.persistance = FuniPersistance(fichier=fichier)
            self.auto_persistance = auto_persistance
            self.auto_calibration = auto_calibration

    @staticmethod
    def _poteaux_liste_a_dict(poteaux: list[Poteau]) -> dict[str, Poteau]:
        """Crée un dict avec la liste de poteaux, en utilisant le nom comme clé"""
        poteaux_dict = {}
        for poteau in poteaux:
            poteaux_dict[poteau.nom] = poteau
        return poteaux_dict
