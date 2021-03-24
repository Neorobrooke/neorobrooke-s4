from __future__ import annotations
from collections import OrderedDict

from typing import Any, Optional
import argparse
import os
import sys
from yaml import load, dump, Loader, Dumper
from pathlib import Path
from traceback import print_exc

from yaml.cyaml import CDumper
from funibot_api.funilib import Poteau, Vecteur

class FuniConfig:
    """Contient la configuration pour un Funibot"""

    def __init__(self, programme: str =  "funibot_" + os.path.basename(__file__)) -> None:
        self.args = self.parse_args(programme=programme)
        self.config = None
        self.generer_config()


    def parse_args(self, programme: str) -> Any:
        """Génère et parse les arguments"""
        parser = argparse.ArgumentParser(
            prog="funibot_" + os.path.basename(programme))
        parser.add_argument('-f', required=True,
                            help='Fichier de config yaml à utiliser')
        parser.add_argument('-p',
                            help='Port série à utiliser (a précédence sur celui dans le fichier de config)')
        parser.add_argument('--mock', action='store_true',
                            help='Mock le port série si présent')

        return parser.parse_args()

    def generer_config(self):
        """Génère les attributs pour chaque option de configuration"""
        self.mock = self.args.mock

        if self.args.f is not None:
            with open(Path(self.args.f), "r") as f:
                self.config = load(f, Loader=Loader)
        else:
            sys.exit("Fichier de config non spécifié")

        if self.args.p is not None:
            self.port = self.args.p
        else:
            try:
                self.port = self.config["serial"]["port"]
            except KeyError:
                sys.exit("Port manquant dans le fichier de config et non spécifié avec -p")

        try:
            self.baud = self.config["serial"]["baudrate"]
        except KeyError:
            sys.exit("Baudrate manquant dans le fichier de config")

        try:
            self.initialiser_poteaux(self.config["poteaux"])
        except KeyError:
            sys.exit("Dictionnaire des poteaux manquant dans le fichier de config")

        try:
            self.sol = self.config["sol"]
        except KeyError:
            sys.exit("Position du sol manquante dans le fichier de config")

    def initialiser_poteaux(self, poteaux: dict) -> None:
        """Initialise la liste de poteaux à partir du dictionnaire de poteaux dans le fichier de config"""
        liste_poteaux = []
        for key, value in poteaux.items():
            try:
                poles = value["poles"]
                accroches = value["accroches"]
                px, py, pz = poles["x"], poles["y"], poles["z"]
                ax, ay, az = accroches["x"], accroches["y"], accroches["z"]
            except KeyError:
                print_exc()
                sys.exit(f"Valeurs manquantes dans le fichier de config pour le poteau [{key}]")

            nouveau_pot = Poteau(nom=key, position_pole=Vecteur(px, py, pz),
                                 position_accroche=Vecteur(ax, ay, az))
            liste_poteaux.append(nouveau_pot)
        self.liste_poteaux = liste_poteaux

    @staticmethod
    def generer_gabarit_config(fichier: Path = Path.cwd() / "config_gabarit.yaml") -> Optional[Path]:
        yaml = """---
  serial:
    port: COM1
    baudrate: 57600
  sol: -1000
  poteaux: # distances en mm
    poteau1:
      poles:
        x: 0
        y: 0
        z: 0
      accroches:
        x: 0
        y: 0
        z: 0
    poteau2:
      poles:
        x: 0
        y: 0
        z: 0
      accroches:
        x: 0
        y: 0
        z: 0
    poteau3:
      poles:
        x: 0
        y: 0
        z: 0
      accroches:
        x: 0
        y: 0
        z: 0
    poteau4:
      poles:
        x: 0
        y: 0
        z: 0
      accroches:
        x: 0
        y: 0
        z: 0
...
"""
        fichier.write_text(yaml)
        return fichier
