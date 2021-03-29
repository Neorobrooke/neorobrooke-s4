from __future__ import annotations
from typing import Union, Tuple, List, Optional
from pathlib import Path
from numbers import Real

from ruamel.yaml import YAML
from typing import OrderedDict

class FuniPersistance:
    def __init__(self, fichier: Union[Path, str]) -> None:
        self.nom_fichier = Path(fichier)
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.explicit_start = True
        self.yaml.explicit_end = True

    def maj(self, poteaux: List[dict], longueurs: List[Real]):
        for data, long in zip(poteaux, longueurs):
            cle = list(data.keys())[0]
            data[cle]["cable"] = long

            self.fichier["poteaux"][cle] = data[cle]

    def calibrer(self, poteaux: List[dict]) -> Optional[List[Real]]:
        longueurs = []
        for pot in poteaux:
            cle = list(pot.keys())[0]
            if cle not in self.fichier["poteaux"].keys():
                return None
            if pot[cle]["poles"] != self.fichier["poteaux"][cle]["poles"]:
                return None
            if pot[cle]["accroches"] != self.fichier["poteaux"][cle]["accroches"]:
                return None
            longueurs.append(self.fichier["poteaux"][cle]["cable"])
        return longueurs

    def _dump(self) -> None:
        with self.nom_fichier.open('w') as f:
            self.yaml.dump(self.fichier, f)
        
    def _load(self) -> OrderedDict:
        with self.nom_fichier.open('r') as f:
            self.fichier = self.yaml.load(f)
        return self.fichier