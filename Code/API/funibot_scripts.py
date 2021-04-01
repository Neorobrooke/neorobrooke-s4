import webbrowser
from sys import prefix
from pathlib import Path


def launch(path: Path) -> None:
    webbrowser.open_new_tab(str(path.absolute()))


dossier = Path(prefix) / "share" / "funibot-neorobrooke"
documentation = dossier / "documentation"
config = dossier / "config.yaml"
erreurs = documentation / "dictionnaireErreur.txt"


def ouvrir_config():
    launch(config)


def ouvrir_erreurs():
    launch(erreurs)


def ouvrir_doc():
    launch(documentation)


def ouvrir_dossier():
    launch(dossier)
