import cmd
import os
from serial import Serial
from serial.serialutil import SerialException
from yaml import load, dump, Loader, Dumper
import argparse
from typing import Any
from serial import Serial
import time
from pprint import pprint
from pathlib import Path

from funibot_api.funibot import Funibot
from funibot_api.funibot_json_serial import FuniSerial

class CLIFunibot(cmd.Cmd):
    intro = "Funibot CLI v1.0   ->   Tapez help ou ? pour la liste des commandes.\n"
    prompt = "(Funibot) $ "

    def __init__(self, port: str, baud: int, completekey: str = 'tab', stdin: Any = None, stdout: Any= None) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        print(port)
        print(baud)
        self.port_serie = port
        self.baud_rate = baud
        try:
            self.serial = Serial(port=port, baudrate=baud)
        except SerialException:
            print("Port série introuvable")
            exit(1)
        self.funi_serial = FuniSerial(self.serial)

    def do_addpoteau(self, arg):
        pass

    def do_makebot(self, arg):
        self.bot = Funibot(self.funi_serial)

    def default(self, arg):
        print("ERREUR: Commande inconnue")

    def do_shell(self, arg):
        os.system(arg)

    def do_echo(self, _):
        print("Test de commande")

    def do_clear(self, _):
        """Efface le terminal"""
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def do_exit(self, _):
        """Ferme le programme"""
        exit(0)

    def do_pos(self, _):
        print(self.bot.pos)

    def do_serial(self, arg):
        self.serial.write(bytes(arg, encoding='utf8'))
        time.sleep(1.2)
        print(str(self.serial.read_all().decode('utf8')))

    def do_load(self, arg):
        with open("config.yaml", "r") as f:
            config_file = load(f, Loader=Loader)
        pprint(config_file)

def parse_args() -> Any:
    parser = argparse.ArgumentParser(prog="funibot_" + os.path.basename(__file__))
    parser.add_argument('-p', help='Port série à utiliser')
    parser.add_argument('-b', help='Baud rate série à utiliser')
    # parser.add_argument('-f', required=True, help='Fichier de config yaml à utiliser')
    parser.add_argument('-f', help='Fichier de config yaml à utiliser')

    return parser.parse_args()

if __name__ == '__main__':
    cli_args = parse_args()
    if cli_args.f is not None:
        with open(Path(cli_args.f), "r") as f:
            config = load(f, Loader=Loader)

    elif cli_args.p is None or cli_args.b is None:
        print("Fichier de config ou port série et baud rate non spécifiés")
        exit(1)

    CLIFunibot(port=config["serial"]["port"], baud=config["serial"]["baudrate"]).cmdloop()