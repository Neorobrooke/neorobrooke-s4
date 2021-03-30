import cmd
import os
import sys
from string import digits
from traceback import print_exc
from serial import Serial
from serial.serialutil import SerialException
from typing import Any
from serial import Serial
import time

from funibot_api.funiconfig import FuniArgs, FuniConfig
from funibot_api.funilib import Direction, Vecteur
from funibot_api.funipersistance import ErreurDonneesIncompatibles
from funibot_api.funiserial import FuniSerial, FuniCommException
from funibot_api.funibot import Funibot
from tests.mock_serial import MockSerial, MockType


class CLIFunibot(cmd.Cmd):
    intro = "Funibot CLI v1.0   ->   Tapez help ou ? pour la liste des commandes.\n"
    prompt = "(Funibot) $ "

    def __init__(self, config: FuniConfig, completekey: str = 'tab', stdin: Any = None, stdout: Any = None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        print(
            f"Ouverture du port série [{config.port}] avec un baudrate de <{config.baud}>")
        self.config = config
        self.port_serie = config.port
        self.baud_rate = config.baud
        self.liste_poteaux = config.liste_poteaux
        if not config.mock:
            try:
                self.serial = Serial(
                    port=config.port, baudrate=config.baud, timeout=10)
            except SerialException:
                sys.exit("Port série introuvable")
        else:
            self.serial = MockSerial(MockType.CLI)

        self.funi_serial = FuniSerial(self.serial)

        try:
            self.bot = Funibot(self.funi_serial, config)
        except ErreurDonneesIncompatibles as e:
            print(e)
            print("Effectuer la calibration manuellement")
        except:
            sys.exit(f"Erreur lors de l'initialisation du bot")

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
            print(
                f"La direction spécifiée n'est pas valide. Ne doit contenir que les caractères [{', '.join('+-xyz')}]")
        else:
            self.bot.deplacer(direction=direction)

    def do_depv(self, arg: str):
        """Déplace dans une direction, jusqu'à la longueur du vecteur indiqué
        La direction est du format "*K1x*K2y*K3z", où les étoiles sont des + (par défaut, peuvent être absents) ou des moins
        Pour ignore une direction, ne pas inclure la lettre.
        Les Ki sont des coefficients réels. S'il est absent, est assumé être 1.

        Exemples:
            - Déplacement en x positif de 12:       "12x" ou "+12x"
            - Déplacement en y négatif de 1:        "-1y" ou "-y"
            - Déplacement oblique en +x et -y:      "x-y" ou "+x-y"
        """
        try:
            direction = Direction(arg)
        except:
            print(
                f"La direction spécifiée n'est pas valide. Ne doit contenir que les caractères [{', '.join(f'+-xyz{digits}')}]")
        else:
            self.bot.deplacer(direction=direction, distance=0)

    def do_depl(self, arg: str):
        """Déplace dans une direction, jusqu'à la longueur indiquée
        La direction est du format "*K1x*K2y*K3z :L", où les étoiles sont des + (par défaut, peuvent être absents) ou des moins
        Pour ignore une direction, ne pas inclure la lettre.
        Les Ki sont des coefficients réels. S'il est absent, est assumé être 1.
        L est la longueur. Si elle est absente, est considérée comme 1.
        Le vecteur nul peut être obtenu avec la valeur spéciale 0, soit comme direction ou comme longueur.

        Exemples:
            - Déplacement en x positif de 12:               "x :12" ou "+x :12"
            - Déplacement en y négatif de 1:                "-y" ou "-y :1"
            - Déplacement oblique en +x et -y de 213:       "x-y :213" ou "+x-y :213"
        """

        try:
            direction, longueur = arg.split(" :")
        except:
            print(f"Format inconnu. Doit être de la forme 'direction :longueur'")
            return

        try:
            direction = Direction(direction)
        except:
            print("La direction spécifiée n'est pas valide. Ne doit contenir que les caractères",
                  f"[{', '.join(f'+-xyz{digits}')}], dont obligatoirement un caractère parmi [{', '.join(f'xyz0')}]")
        else:
            try:
                longueur = float(longueur)
            except ValueError:
                print(f"Erreur: 'longueur' doit être un nombre réel")
            else:
                self.bot.deplacer(direction=direction, distance=longueur)

    def do_stop(self, _):
        """Arrête le mouvement du robot"""
        self.bot.stop()

    def default(self, _):
        """Appelé pour une commande inconnue"""
        print("ERREUR: Commande inconnue")

    def emptyline(self):
        pass

    def do_err(self, _):
        """Affiche la liste des erreurs en provenance du OpenCR
           Format -> FuniErreur<timestamp>(M)[code:NOM_ERREUR]

           * La partie "(M)" signifie "erreur majeure", et n'est pas affichée pour une erreur mineure
        """
        try:
            erreurs = self.bot.erreur()
        except:
            print_exc()
            raise

        if erreurs is not None:
            for item in erreurs:
                print(item)
        else:
            print("")

    def do_shell(self, arg):
        """Exécute la commande dans le shell sous-jacent. S'utilise aussi avec ! suivi de la commande."""
        os.system(arg)

    def do_clear(self, _):
        """Efface le terminal"""
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def do_exit(self, _):
        """Ferme le programme"""
        # La destruction du Funibot avant de quitter permet d'y mettre un breakpoint
        # Cela permet de déboguer le __del__ du Funibot
        del self.bot
        sys.exit()

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
                print(
                    "Ne pas mettre de ':' pour utiliser l'identifiant du poteau tel qu'indiqué dans le fichier de configuration")
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
                print(
                    f"Préfixer l'argument avec ':' pour utiliser un index de poteau entre 0 et {len(self.liste_poteaux) - 1}")

    def do_len(self, arg):
        """Affiche la longueur des câbles.
           Format de la commande:
               'len'                -> Affiche tous les poteaux
               'len nom_poteau'     -> Affiche seulement un poteau selon son nom dans le fichier de config
               'len :id_poteau'     -> Affiche seulement un poteau selon son id entier attribué par le OpenCR
           Format de la sortie:
               Câble[id:nom] -> longueur
               id est -1 si le poteau n'est pas initialisé au niveau du OpenCR
        """
        if arg == "":
            for poteau in self.bot.values():
                print(poteau.repr_cable())
        elif ':' in arg:
            _, num = arg.split(':')
            try:
                print(self.bot.poteaux_id[int(num)].repr_cable())
            except ValueError:
                print(
                    f"L'index doit être un entier entre 0 et {len(self.liste_poteaux) - 1}")
                print(
                    "Ne pas mettre de ':' pour utiliser l'identifiant du poteau tel qu'indiqué dans le fichier de configuration")
                return
            except IndexError:
                print(
                    f"Index inconnu, doit être entre 0 et {len(self.liste_poteaux) - 1}")
                return
        else:
            try:
                print(self.bot[arg].repr_cable())
            except KeyError:
                print("Identifiant de poteau inconnu.")
                print(f"Choisir parmi [{', '.join(self.bot.keys())}]")
                print(
                    f"Préfixer l'argument avec ':' pour utiliser un index de poteau entre 0 et {len(self.liste_poteaux) - 1}")

    def do_go(self, arg: str):
        """Déplace le robot à la position x:y:z donnée.
           Format: 'go x:y:z' avec x, y et z les composantes du vecteur position, en mm. 
           Le vecteur position est dans le même référentiel que les vecteurs dans le fichier de config.
        """
        try:
            px, py, pz = arg.split(":")
        except ValueError:
            print(
                "Pas le bon nombre d'arguments, il faut trois nombres sous la forme x:y:z")
            return

        try:
            px, py, pz = int(px), int(py), int(pz)
        except ValueError:
            print(
                f"Les arguments doivent être trois nombres -> reçu <{px}:{py}:{pz}>")
            return

        try:
            self.bot.pos = Vecteur(px, py, pz)
        except FuniCommException:
            print_exc()

    def do_cal(self, _):
        # """[PAS IMPLÉMENTÉ] Calibre automatiquement le Funibot"""
        """Calibre automatiquement le Funibot selon le fichier de persistance de la calibration.
           Ce fichier est indiqué dans le fichier de configuration.
           Il peut aussi provenir d'un argument.
        """
        # print("ERREUR: Pas implémenté")
        try:
            self.bot.calibrer()
        except ErreurDonneesIncompatibles as e:
            print("Impossible de calibrer", end=": ")
            print(e)

    def do_persi(self, _):
        """Enregistre la calibration du Funibot dans le fichier de persistance de la calibration.
           Ce fichier est indiqué dans le fichier de configuration.
           Il peut aussi provenir d'un argument.
        """
        self.bot.enregister_calibration()

    def do_sol(self, _):
        """Affiche la position actuelle du sol"""
        print(self.bot.repr_sol())

    def do_chsol(self, arg):
        """Modifie la position actuelle du sol"""
        try:
            self.bot.sol = float(arg)
        except ValueError:
            print("La position du sol doit être un nombre réel")
        except FuniCommException:
            print_exc()
        else:
            print(self.bot.repr_sol())


if __name__ == '__main__':
    args = FuniArgs().generer_config()
    cli_funibot = CLIFunibot(config=args.config)

    cli_funibot.cmdloop()
