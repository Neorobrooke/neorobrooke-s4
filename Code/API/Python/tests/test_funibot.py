from __future__ import annotations
import unittest

from funibot_api.funiconfig import FuniConfig
from funibot_api.funilib import Poteau, Vecteur
from funibot_api.funiserial import FuniSerial
from funibot_api.funibot import Funibot
from tests.mock_serial import MockSerial, DualMockSerial, MockType


class TestsFunibot(unittest.TestCase):
    """Tests sur la classe Funibot de funibot_api"""

    def setUp(self) -> None:
        """Initialisation commune à plusieurs tests"""
        self.mock = MockSerial(MockType.TEST)
        self.serial = FuniSerial(self.mock)

        self.emock = MockSerial(MockType.TEST)
        self.dmock = DualMockSerial(
            canal_lecture=self.mock, canal_ecriture=self.emock)
        self.dserial = FuniSerial(self.dmock)

        self.poteaux = [Poteau("pot1", Vecteur(x=1, y=2, z=3), Vecteur(x=11, y=12, z=13)),
                        Poteau("pot2", Vecteur(x=4, y=5, z=8), Vecteur(x=0, y=23, z=9))]

        self.config = FuniConfig()
        self.config.liste_poteaux = self.poteaux
        self.config.sol = 0

    def test_init(self):
        """Test d'initialisation d'un Funibot"""
        bot = Funibot(self.serial, config=self.config)

        self.assertEqual(self.poteaux, list(bot.poteaux.values()))
        self.assertEqual(len(bot.poteaux_id), len(self.poteaux))

    def test_repr(self):
        """Test de représentation d'un Funibot"""
        bot = Funibot(self.serial, config=self.config)

        self.assertEqual(repr(
            bot), "Funibot[Mock]([Poteau[0:pot1](1;2;3)(11;12;13), Poteau[1:pot2](4;5;8)(0;23;9)])", msg="")

    def test_pos(self):
        bot = Funibot(self.dserial, config=self.config)
        position = Vecteur(12, 45, -647234)

        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "pos", "type": "ack", "args": {{"pos_x": {position.x}, "pos_y": {position.y}, "pos_z": {position.z}}}}}', 'utf8')

        val_position = bot.pos

        self.assertEqual(position, val_position,
                         msg=f"Position est {position} au lieu de {val_position}")

    def test_pos_none(self):
        """Test de position de None"""
        bot = Funibot(self.dserial, config=self.config)
        position = Vecteur()

        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "pos", "type": "set", "args": {{"pos_x": {position.x}, "pos_y": {position.y}, "pos_z": {position.z}}}}}', 'utf8')

        val_position = bot.pos

        self.assertIsNone(
            val_position, msg=f"Position est {val_position} au lieu d'être None")

    def test_set_pos(self):
        bot = Funibot(self.dserial, config=self.config)
        position = Vecteur(12, 45, -647234)

        bot.pos = position

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "set", "args": {{"pos_x": {position.x}, "pos_y": {position.y}, "pos_z": {position.z}}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"Position est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_sol(self):
        bot = Funibot(self.dserial, config=self.config)

        bot.sol = 34
    
        self.assertEqual(bot.sol, bot._sol,
                         msg=f"Position du sol est {bot.sol} au lieu de {bot._sol}")

    def test_set_sol(self):
        bot = Funibot(self.serial, config=self.config)
        long = 12
        bot.sol = long

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "sol", "id": null, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Position du sol est {validation_requete} au lieu de {self.mock.requete}")

    def test_getitem(self):
        bot = Funibot(self.dserial, config=self.config)
    
        nom = "pot1"
        self.assertIs(bot[nom], bot.poteaux[nom],
                         msg=f"Le nom du poteau est {bot[nom]} au lieu de {bot.poteaux[nom]}")

    def test_keys(self):
        bot = Funibot(self.dserial, config=self.config)

        self.assertTrue(bot.keys() == bot.poteaux.keys(),
                         msg=f"La clé du poteau est {bot.keys()} au lieu de {bot.poteaux.keys()}")

    def test_values(self):
        bot = Funibot(self.dserial, config=self.config)

        self.assertTrue(list(bot.values()) == list(bot.poteaux.values()),
                         msg=f"La valeur du poteau est {list(bot.values())} au lieu de {list(bot.poteaux.values())}")

    def test_items(self):
        bot = Funibot(self.dserial, config=self.config)

        self.assertTrue(bot.items() == bot.poteaux.items(),
                         msg=f"Les items du poteau sont {bot.items()} au lieu de {bot.poteaux.items()}")

    def test_iter(self):
        bot = Funibot(self.dserial, config=self.config)

        self.assertTrue(list(bot) == list(bot.poteaux.values()),
                         msg=f"L'iteration du poteau est {list(bot)} au lieu de {list(bot.poteaux.values())}")

    def test_set_stop(self):
        bot = Funibot(self.dserial, config=self.config)
        bot.stop()

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "stop", "axe_x": null, "axe_y": null, "axe_z": null}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"Après avoir demandé l'arrêt, la position est {validation_requete} au lieu de {self.dmock.ecriture.requete}")
 

