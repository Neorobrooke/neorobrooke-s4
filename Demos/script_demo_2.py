from __future__ import annotations

from serial import Serial
import time
from funibot_api import Funibot, FuniArgs, FuniSerial, Vecteur
from funibot_api.funimock import MockSerial, eMockType
from funibot_api.funiserial import eFuniRegime


def script(bot: Funibot):
    
    print()
    print("Affichage de la position actuelle:")
    print(f"Position: {bot.pos}")
    print()

    bot.sol = -1000    
    
    centre = Vecteur(610, -700, 610)
    pos1 = Vecteur(100, -700, 610)
    pos2 = Vecteur(100, -700, 100)
    pos3 = Vecteur(100, -400, 100)
    coin = Vecteur(800, -700, 800)

    positions = [centre, pos1, pos2, pos3, coin]

    print("Affichage des poteaux:")
    for poteau in bot.poteaux.values():
        print(poteau)

    print()

    with bot.tout_attendre() as att:
        for pos in positions:
            print(f"Déplacement à la position {pos}:")
            print("...")
            bot.pos = pos
            print("Arrivé!")
            print(f"Position: {bot.pos}")
            print()

    print()

    print("Retour de la dernière attente:")
    print(f"Méthode: {att[-1].nom_methode}")
    print(f"Retour: {att[-1].retour_attendre}")
    print()

    print("Désactivation des moteurs:")
    bot.moteurs_actifs = False
    print("Attente de 5 secondes...")
    time.sleep(5)
    print("Réactivation des moteurs.")
    bot.moteurs_actifs = True
    print()

    print(f"Retour au centre:")
    bot.pos = centre
    print(f"Durée minimale estimée: {bot.duree_minimale} s")
    t1 = time.time()
    print("...")
    bot.attendre()
    tf = time.time() - t1
    print("Arrivé!")
    print(f"Position: {bot.pos}")
    print(f"Durée du déplacement: {tf} s")
    print()

    time.sleep(3)

    print("On monte jusqu'à ce qu'on sorte de la zone:")
    bot.deplacer("y")
    
    while bot.regime is not eFuniRegime.ARRET:
        time.sleep(1)
    
    print()

    print("Affichage des erreurs:")
    for err in bot.erreurs():
        print(err)
    print()

    print("Fin de la démo")
    

def main():
    args = FuniArgs("script_demo_2").generer_config()
    if args.config.mock:
        _serial = MockSerial(type=eMockType.TEST)
    else:
        _serial = Serial(port=args.config.port, baudrate=args.config.baud)
    serial = FuniSerial(serial=_serial)
    bot = Funibot(serial=serial, config=args.config)

    # bot.calibrer()
    # bot.moteurs_actifs = False
    # input()
    # bot.moteurs_actifs = True

    script(bot=bot)
    bot.enregister_calibration()


if __name__ == '__main__':
    main()
