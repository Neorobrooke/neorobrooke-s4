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

from funibot_api.funibot import Direction, FuniCommException, Funibot, Poteau, Vecteur
from funibot_api.funibot_json_serial import FuniModeCalibration, FuniSerial, FuniType, MockSerial


class CLIFunibot(cmd.Cmd):
    intro = "Funibot CLI v1.0   ->   Tapez help ou ? pour la liste des commandes.\n"
    prompt = "(Funibot) $ "

    def __init__(self, port: str, baud: int, mock: bool = False, completekey: str = 'tab', stdin: Any = None, stdout: Any = None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        print(f"Ouverture du port série [{port}] avec un baudrate de <{baud}>")
        self.port_serie = port
        self.baud_rate = baud
        if not mock:
            try:
                self.serial = Serial(port=port, baudrate=baud, timeout=10)
            except SerialException:
                print("Port série introuvable")
                exit(1)
        else:
            self.serial = MockSerial()

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
        self.liste_poteaux = liste_poteaux
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
            except ValueError:
                print(f"La longueur doit être un nombre -> reçu [{valeur}]")

    def do_dep(self, arg: str):
        """Déplace dans une direction, jusqu'à ce que la commande "stop" soit envoyée
           La direction est du format "*x*y*z", où les étoiles sont des + (par défaut, peuvent être absents) ou des moins
           Pour ignore une direction, ne pas inclure la lettre.

           Exemples:
             - Déplacement en x positif:            "x" ou "+x"
             - Déplacement en y négatif:            "-y"
             - Déplacement oblique en +x et -y:     "x-y" ou "+x-y"
        """
        try:
            direction = Direction(arg)
        except:
            print(f"La direction spécifiée n'est pas valide. Ne doit contenir que les caractères [{', '.join('+-xyz')}]")
        else:
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

    def do_ls(self, arg):
        """Liste les poteaux et leurs positions.
           Format de la commande:
               'ls'                 -> Affiche tous les poteaux
               'ls nom_poteau'      -> Affiche seulement un poteau selon son nom dans le fichier de config
               'ls :id_poteau'      -> Affiche seulement un poteau selon son id entier attribué par le OpenCR
           Format de la sortie (identique au __repr__ de la classe Poteau du module funibot):
               Poteau[id:nom](px;py;pz)(ax;ay;az)
               id est -1 si le poteau n'est pas initialisé au niveau du OpenCR
               Le vecteur (px;py;pz) représente la position du poteau
               Le vecteur (ax;ay;az) représente la position de l'attache sur la nacelle par rapport au TCP du robot
               (Le TCP est le Tool Center Point)
        """
        if arg == "":
            for poteau in self.bot.values():
                print(poteau)
        elif ':' in arg:
            _, num = arg.split(':')
            try:
                print(self.bot.poteaux_id[int(num)])
            except ValueError:
                print(
                    f"L'index doit être un entier entre 0 et {len(self.liste_poteaux) - 1}")
                print("Ne pas mettre de ':' pour utiliser l'identifiant du poteau tel qu'indiqué dans le fichier de configuration")
                return
            except IndexError:
                print(
                    f"Index inconnu, doit être entre 0 et {len(self.liste_poteaux) - 1}")
                return
        else:
            try:
                print(self.bot[arg])
            except KeyError:
                print("Identifiant de poteau inconnu.")
                print(f"Choisir parmi [{', '.join(self.bot.keys())}]")
                print(f"Préfixer l'argument avec ':' pour utiliser un index de poteau entre 0 et {len(self.liste_poteaux) - 1}")

    def do_go(self, arg: str):
        """Déplace le robot à la position x:y:z donnée.
           Format: 'go x:y:z' avec x, y et z les composantes du vecteur position, en mm. 
           Le vecteur position est dans le même référentiel que les vecteurs dans le fichier de config.
        """
        try:
            px, py, pz = arg.split(":")
        except ValueError:
            print("Pas le bon nombre d'arguments, il faut trois nombres sous la forme x:y:z")
            return
        
        try:
            px, py, pz = int(px), int(py), int(pz)
        except ValueError:
            print(f"Les arguments doivent être trois nombres -> reçu <{px}:{py}:{pz}>")
            return

        try:
            self.bot.pos = Vecteur(px, py, pz)
        except FuniCommException as e:
            print_exc()

    def do_cal(self, arg):
        """[PAS IMPLÉMENTÉ] Calibre automatiquement le Funibot"""
        print("ERREUR: Pas implémenté")


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="funibot_" + os.path.basename(__file__))
    parser.add_argument('-f', required=True,
                        help='Fichier de config yaml à utiliser')
    parser.add_argument('--mock', action='store_true',
                        help='Mock le port série si présent')

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

    cli_funibot = CLIFunibot(port=port, baud=baud, mock=cli_args.mock)
    try:
        cli_funibot.initialiser_poteaux(config["poteaux"])
    except KeyError:
        print_exc()
        print("Dictionnaire des poteaux manquant dans le fichier de config")
        exit(3)

    cli_funibot.cmdloop()
