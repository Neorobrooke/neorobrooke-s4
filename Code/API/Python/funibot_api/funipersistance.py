from __future__ import annotations
from typing import Union
from pathlib import Path

from ruamel.yaml import YAML
from typing import OrderedDict

class FuniPersistance:
    def __init__(self, fichier: Union[Path, str]) -> None:
        self.nom_fichier = Path(fichier)
        self.yaml = YAML()
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.explicit_start = True
        self.yaml.explicit_end = True

    def generer_yaml(self, donnees: dict):
        pass

    def _dump(self) -> None:
        with self.nom_fichier.open('w') as f:
            self.yaml.dump(self.fichier, f)
        
    def _load(self) -> OrderedDict:
        with self.nom_fichier.open('r') as f:
            self.fichier = self.yaml.load(f)
        return self.fichier