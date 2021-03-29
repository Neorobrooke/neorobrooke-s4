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
        for poteau, longueur in zip(poteaux, longueurs):
            cle = list(poteau.keys())[0]
            poteau[cle]["cable"] = longueur

            self.fichier["poteaux"][cle] = poteau[cle]

    def calibrer(self, poteaux: List[dict]) -> Optional[Dict[str, float]]:
        """Retourne un dictionnaire contenant les valeurs permettant de calibrer le Funibot"""
        longueurs = dict()
        for poteau in poteaux:
            cle = list(poteau.keys())[0]
            if cle not in self.fichier["poteaux"].keys():
                raise ErreurDonneesIncompatibles(f"{cle} n'est pas dans le fichier")
            if poteau[cle]["poles"] != self.fichier["poteaux"][cle]["poles"]:
                raise ErreurDonneesIncompatibles(f"Les pôles pour {cle} ne correspondent pas")
            if poteau[cle]["accroches"] != self.fichier["poteaux"][cle]["accroches"]:
                raise ErreurDonneesIncompatibles(f"Les accroches pour {cle} ne correspondent pas")
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