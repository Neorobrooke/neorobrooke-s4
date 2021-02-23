import cmd
import os
from traceback import print_exc
from serial import Serial
from serial.serialutil import SerialException
from yaml import load, dump, Loader, Dumper
import argparse
from typing import Any
from serial import Serial
import time
from pprint import pprint
from pathlib import Path

from funibot_api.funibot import Direction, Funibot, Poteau, Vecteur
from funibot_api.funibot_json_serial import FuniModeCalibration, FuniSerial, FuniType


class CLIFunibot(cmd.Cmd):
    intro = "Funibot CLI v1.0   ->   Tapez help ou ? pour la liste des commandes.\n"
    prompt = "(Funibot) $ "

    def __init__(self, port: str, baud: int, completekey: str = 'tab', stdin: Any = None, stdout: Any = None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        print(port)
        print(baud)
        self.port_serie = port
        self.baud_rate = baud
        try:
            self.serial = Serial(port=port, baudrate=baud, timeout=10)
        except SerialException:
            print("Port série introuvable")
            exit(1)

        self.funi_serial = FuniSerial(self.serial)

    def initialiser_poteaux(self, poteaux: dict) -> None:
        liste_poteaux = []
        for key, value in poteaux.items():
            try:
                poles = value["poles"]
                accroches = value["accroches"]
                px, py, pz = poles["x"], poles["y"], poles["z"]
                ax, ay, az = accroches["x"], accroches["y"], accroches["z"]
            except KeyError:
                print_exc()
                print(
                    f"Valeurs manquantes dans le fichier de config pour le poteau [{key}]")
                exit(4)

            nouveau_pot = Poteau(nom=key, position_pole=Vecteur(px, py, pz),
                                 position_accroche=Vecteur(ax, ay, az))
            liste_poteaux.append(nouveau_pot)

        try:
            self.bot = Funibot(self.funi_serial, liste_poteaux)
        except:
            print(f"Erreur lors de l'initialisation du bot")
            exit(5)

    def do_cable(self, arg: str):
        """Calibre en posant la longueur d'un ou de plusieurs cables
           Format -> cable nom_poteau_1:longueur_1 [nom_poteau2:longueur2 ...]
        """
        cables = arg.split(" ")
        for cable in cables:
            try:
                cle, valeur = cable.split(":")
            except:
                print("Doit être une entrée de la forme idpoteau:longueur")
                return
            try:
                self.bot.poteaux[cle].longueur_cable = float(valeur)
            except KeyError as e:
                print(f"Erreur: {e}")
                return

    def do_dep(self, arg: str):
        """Déplace dans une direction, jusqu'à ce que la commande "stop" soit envoyée
           La direction est du format "*x*y*z", où les étoiles sont des + (par défaut, peuvent être absents) ou des moins
           Pour ignore une direction, ne pas inclure la lettre.
           
           Exemples:
             - Déplacement en x positif:            "x" ou "+x"
             - Déplacement en y négatif:            "-y"
             - Déplacement oblique en +x et -y:     "x-y" ou "+x-y"
        """
        direction = Direction(arg)
        self.bot.deplacer_vers(direction=direction)

    def do_stop(self, _):
        """Arrête le mouvement du robot"""
        self.bot.stop()

    def default(self, _):
        """Appelé pour une commande inconnue"""
        print("ERREUR: Commande inconnue")

    def do_err(self, _):
        """Affiche la liste des erreurs en provenance du OpenCR
           Format -> FuniErreur<timestamp>(M)[code:NOM_ERREUR]
           
           * La partie "(M)" signifie "erreur majeure", et n'est pas affichée pour une erreur mineure
        """
        try:
            erreurs = self.bot.erreur()
        except:
            print_exc()

        for item in erreurs[0]:
            print(item)

    def do_shell(self, arg):
        """Exécute la commande dans le shell sous-jacent. S'utilise aussi avec ! suivi de la commande."""
        os.system(arg)

    def do_clear(self, _):
        """Efface le terminal"""
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def do_exit(self, _):
        """Ferme le programme"""
        exit(0)

    def do_pos(self, _):
        """Demande et affiche la position du robot"""
        print(self.bot.pos)

    def do_serial(self, arg):
        """Envoie une commande série directement au OpenCR, et affiche la réponse"""
        self.serial.write(bytes(arg, encoding='utf8'))
        time.sleep(1.2)
        print(str(self.serial.read_all().decode('utf8')))

    def do_(self, arg):
        pass


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="funibot_" + os.path.basename(__file__))
    parser.add_argument('-f', required=True,
                        help='Fichier de config yaml à utiliser')

    return parser.parse_args()


if __name__ == '__main__':
    cli_args = parse_args()
    if cli_args.f is not None:
        with open(Path(cli_args.f), "r") as f:
            config = load(f, Loader=Loader)
    else:
        print("Fichier de config non spécifié")
        exit(1)

    try:
        port = config["serial"]["port"]
        baud = config["serial"]["baudrate"]
    except KeyError:
        print_exc()
        print("Port ou baudrate manquants dans le fichier de config")
        exit(2)

    cli_funibot = CLIFunibot(port=port, baud=baud)
    try:
        cli_funibot.initialiser_poteaux(config["poteaux"])
    except KeyError:
        print_exc()
        print("Dictionnaire des poteaux manquant dans le fichier de config")
        exit(3)

    cli_funibot.cmdloop()
