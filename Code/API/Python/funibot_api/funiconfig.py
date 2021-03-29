from __future__ import annotations

from typing import Optional, List, Union
import argparse
import os
import sys
from ruamel.yaml.events import NodeEvent
from yaml import load, Loader
from pathlib import Path
from traceback import print_exc

from funibot_api.funilib import Poteau, Vecteur
from funibot_api.funipersistance import FuniPersistance


class FuniConfig:
    """Contient la configuration pour un Funibot"""

    def __init__(self) -> None:
        self.mock = None
        self.yaml = None
        self.port = None
        self.baud = None
        self.sol = None
        self.persistance = None
        self.liste_poteaux = []

    def generer_config(self, fichier: Union[Path, str], mock: bool,
                       auto_persistance: Optional[bool] = None,
                       auto_calibration: Optional[bool] = None,
                       port: str = None,
                       persistance: Union[Path, str] = None) -> FuniConfig:
        """Génère les attributs pour chaque option de configuration"""
        self.mock = (mock == True)

        with open(fichier, "r") as f:
            self.config = load(f, Loader=Loader)

        if port is not None:
            self.port = port
        else:
            try:
                self.port = self.config["serial"]["port"]
            except KeyError:
                sys.exit(
                    "Port manquant dans le fichier de config et non spécifié en argument")

        if persistance is not None:
            self.persistance = Path(persistance)
        else:
            try:
                self.persistance = Path(self.config["persistance"]["fichier"])
            except KeyError:
                self.persistance = None

        if auto_persistance is not None:
            self.auto_persistance = (auto_persistance == True)
        else:
            try:
                self.auto_persistance = (self.config["persistance"]["auto-persistance"] == True)
            except KeyError:
                self.auto_persistance = False

        if auto_calibration is not None:
            self.auto_calibration = (auto_calibration == True)
        else:
            try:
                self.auto_calibration = (self.config["persistance"]["auto-calibration"] == True)
            except KeyError:
                self.auto_calibration = False

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

        return self

    def initialiser_poteaux(self, poteaux: List[dict]) -> None:
        """Initialise la liste de poteaux à partir du dictionnaire de poteaux dans le fichier de config"""
        liste_poteaux = []
        for poteau in poteaux:
            key = list(poteau.keys())[0]
            value = list(poteau.values())[0]
            try:
                poles = value["poles"]
                accroches = value["accroches"]
                px, py, pz = poles["x"], poles["y"], poles["z"]
                ax, ay, az = accroches["x"], accroches["y"], accroches["z"]
            except KeyError:
                print_exc()
                sys.exit(
                    f"Valeurs manquantes dans le fichier de config pour le poteau [{key}]")

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
  persistance:
    fichier: Code/API/Python/calibration.yaml
    auto-persistance: False
    auto-calibration: False
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


class FuniArgs:
    """Gère les arguments CLI par défaut pour le Funibot"""

    def __init__(self, programme: str = "funibot_api." + os.path.basename(__file__)) -> None:
        """Génère et parse les arguments"""
        self.parser = argparse.ArgumentParser(prog=programme)
        self.parser.add_argument('-f', required=True,
                                 help='Fichier de config yaml à utiliser')
        self.parser.add_argument('-c',
                                 help='Fichier de persistance de la calibration yaml à utiliser (a précédence sur celui dans le fichier de config)')
        self.parser.add_argument('-p',
                                 help='Port série à utiliser (a précédence sur celui dans le fichier de config)')
        self.parser.add_argument('--mock', action='store_true',
                                 help='Mock le port série si présent')
        self.parser.add_argument('--auto-persistance', action='store_true',
                                 help='Enregistre la calibration à la fermeture')
        self.parser.add_argument('--auto-calibration', action='store_true',
                                 help="Calibre selon le fichier de persistance à l'ouverture")

        self.args = self.parser.parse_args()

    def generer_config(self) -> FuniArgs:
        """Génère les attributs pour chaque option de configuration"""
        self.config = FuniConfig()

        if self.args.f is not None:
            self.config.generer_config(
                fichier=Path(self.args.f),
                mock=self.args.mock,
                port=self.args.p,
                auto_calibration=self.args.auto_calibration,
                auto_persistance=self.args.auto_persistance,
                persistance=self.args.c)
        else:
            sys.exit("Fichier de config non spécifié")

        return self
