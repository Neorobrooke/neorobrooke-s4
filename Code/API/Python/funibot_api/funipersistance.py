from __future__ import annotations
from typing import Union, List, Optional, Dict, OrderedDict
from pathlib import Path

from ruamel.yaml import YAML
from typing import OrderedDict


class ErreurDonneesIncompatibles(Exception):
    pass


class FuniPersistance:
    """Représente un fichier de persistance de la calibration"""
    def __init__(self, fichier: Union[Path, str]) -> None:
        """Instancie un FuniPersistance lié à un fichier de persistance"""
        self.nom_fichier = Path(fichier)
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.explicit_start = True
        self.yaml.explicit_end = True

    def enregistrer(self, poteaux: List[dict], longueurs: List[float]):
        """Enregistre la calibration actuelle dans le fichier de persistance"""
        try:
            self._load()
        except:
            self._generer(poteaux, longueurs)
        else:
            for poteau, longueur in zip(poteaux, longueurs):
                cle = list(poteau.keys())[0]
                if longueur is None:
                    raise ErreurDonneesIncompatibles(f"La longueur actuelle du câble pour [{cle}] est None")
                poteau[cle]["cable"] = longueur

            for poteau in poteaux:
                cle = list(poteau.keys())[0]
                self.fichier["poteaux"][cle] = poteau[cle]
        self._dump()

    def calibrer(self, poteaux: List[dict]) -> Optional[Dict[str, float]]:
        """Retourne un dictionnaire contenant les valeurs permettant de calibrer le Funibot"""
        self._load()
        longueurs = dict()
        for poteau in poteaux:
            cle = list(poteau.keys())[0]
            if cle not in self.fichier["poteaux"].keys():
                raise ErreurDonneesIncompatibles(f"[{cle}] n'est pas dans le fichier")
            if poteau[cle]["poles"] != self.fichier["poteaux"][cle]["poles"]:
                raise ErreurDonneesIncompatibles(f"Les pôles pour [{cle}] ne correspondent pas")
            if poteau[cle]["accroches"] != self.fichier["poteaux"][cle]["accroches"]:
                raise ErreurDonneesIncompatibles(f"Les accroches pour [{cle}] ne correspondent pas")
            if self.fichier["poteaux"][cle]["cable"] is None:
                raise ErreurDonneesIncompatibles(f"La longueur du câble pour [{cle}] dans le fichier est None")
            longueurs[cle] = self.fichier["poteaux"][cle]["cable"]
        return longueurs

    def _dump(self) -> None:
        """Écrit la calibration dans le fichier"""
        with self.nom_fichier.open('w') as f:
            self.yaml.dump(self.fichier, f)
        
    def _load(self) -> OrderedDict:
        """Lit la calibration du fichier"""
        with self.nom_fichier.open('r') as f:
            self.fichier = self.yaml.load(f)
        return self.fichier

    def _generer(self, poteaux: List[dict], longueurs: List[float]):
        """Génère un fichier de persistance"""
        dict_poteaux = {}
        for item, longueur in zip(poteaux, longueurs):
            cle = list(item.keys())[0]
            item[cle]["cable"] = longueur
            dict_poteaux[cle] = item[cle]
        self.fichier = {}
        self.fichier["poteaux"] = dict_poteaux
        self._dump()
        self._load()