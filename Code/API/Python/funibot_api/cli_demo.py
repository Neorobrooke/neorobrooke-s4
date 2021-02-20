# from funibot_api.funibot_json_serial import (FuniSerial, FuniModeDeplacement,
                                            #  FuniModeCalibration, FuniType)

import funibot_api.funibot

import cmd
import os
from serial import Serial
from yaml import load, dump

class CLIFunibot(cmd.Cmd):
    intro = "Funibot CLI v1.0   ->   Tapez help ou ? pour la liste des commandes.\n"
    prompt = "(Funibot) $ "

    def do_echo(self):
        print("test de commande")

    def do_ls(self):
        os.system('ls -la')

if __name__ == '__main__':
    CLIFunibot().cmdloop()