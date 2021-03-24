from __future__ import annotations
import unittest

from funibot_api.funiconfig import FuniConfig
from funibot_api.funilib import Poteau, Vecteur
from funibot_api.funibot_json_serial import FuniSerial
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
        position = Vecteur(12,45,-647234)

        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "pos", "type": "ack", "args": {{"pos_x": {position.x}, "pos_y": {position.y}, "pos_z": {position.z}}}}}', 'utf8')

        val_position = bot.pos

        self.assertEqual(position, val_position, msg=f"Position est {position} au lieu de {val_position}")

    def test_set_pos(self):
        bot = Funibot(self.dserial, config=self.config)
        position = Vecteur(12,45,-647234)

        bot.pos = position

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "set", "args": {{"pos_x": {position.x}, "pos_y": {position.y}, "pos_z": {position.z}}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete, msg=f"Position est {validation_requete} au lieu de {self.dmock.ecriture.requete}")
