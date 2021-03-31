from __future__ import annotations
from typing import Tuple

from funibot_api.funiserial import FuniErreur, FuniSerial, FuniType, eFuniErreur
from tests.mock_serial import MockSerial, MockType, DualMockSerial
import unittest

class TestFuniErreur(unittest.TestCase):
    """Tests sur la classe FuniErreur"""
    
    def CreationTexte(self):
        pass

    def CreationEntier(self):
        pass

    def Representation(self):
        pass

class TestsFuniSerial(unittest.TestCase):
    """Test sur la classe FuniSerial"""

    def setUp(self):
        """Initialisation commune à plusieurs tests"""
        self.mock = MockSerial(MockType.TEST)
        self.emock = MockSerial(MockType.TEST)
        self.dmock = DualMockSerial(canal_lecture=self.mock, canal_ecriture=self.emock)

    def test_repr(self):
        """Test de représentation d'un FuniSerial"""
        bot = FuniSerial(self.mock)

        self.assertEqual(repr(
            bot), "Mock", msg = f"La représentation du FuniSerial est {repr(bot)} au lieu de Mock")

    def test_pot(self):
        """Test du poteau du FuniSerial"""
        bot = FuniSerial(self.mock)
        position = (3,1.2,8)
        bot.pot(FuniType.SET,0,position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "set", "args": {{"id": 0, "pos_x": {position[0]}, "pos_y": {position[1]}, "pos_z": {position[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_id_float(self):
        """Test du poteau du FuniSerial avec un float comme id"""
        bot = FuniSerial(self.mock)
        position = (3,1.2,8)

        with self.assertRaises(TypeError, msg = "La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            bot.pot(FuniType.SET,1.4,position)
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_pot_err_id_neg(self):
        """Test du poteau du FuniSerial avec un négatif comme id"""
        bot = FuniSerial(self.mock)
        position = (3,1.2,8)

        with self.assertRaises(ValueError, msg = "La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            bot.pot(FuniType.SET,-2,position)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

