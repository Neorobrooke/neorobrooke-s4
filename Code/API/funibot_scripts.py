import webbrowser
from sys import prefix
from pathlib import Path
from shutil import copy, copytree


def launch(path: Path) -> None:
    webbrowser.open_new_tab(str(path.absolute()))


dossier = Path(prefix) / "share" / "funibot-neorobrooke"
documentation = dossier / "Documentation"
config = dossier / "config.yaml"
calibration = dossier / "calibration.yaml"
erreurs = documentation / "dictionnaire_erreurs.txt"


def ouvrir_erreurs():
    launch(erreurs)


def ouvrir_doc():
    launch(documentation)


def copier_config():
    copy(str(config), ".")
    copy(str(calibration), ".")


def copier_doc():
    copytree(str(documentation), "./documentation")
