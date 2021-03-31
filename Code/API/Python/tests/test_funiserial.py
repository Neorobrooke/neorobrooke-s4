from __future__ import annotations
from typing import Tuple

from funibot_api.funiserial import FuniErreur, FuniModeCalibration, FuniModeDeplacement, FuniSerial, FuniType, eFuniErreur
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

    def test_pot_err_pos_none(self):
        """Test du poteau du FuniSerial avec une position None"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(ValueError, msg = "La présence de None comme position n'a pas levé d'exception de type ValueError") as re:
            bot.pot(FuniType.SET,2,position)
        self.assertEqual(str(re.exception), "position est None")

    def test_pot_get(self):
        """Test du poteau du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        position = (3,1.2,8)
        bot.pot(FuniType.GET,0,position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "get", "args": {{"id": 0, "pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(TypeError, msg = "La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.pot(FuniModeDeplacement.START,2,position)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_cal_sol(self):
        """Test de calibration du sol du FuniSerial"""
        bot = FuniSerial(self.mock)
        long = 4.3
        bot.cal(FuniType.SET,FuniModeCalibration.SOL,0,long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "sol", "id": null, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration du sol est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_cable(self):
        """Test de calibration des cables du FuniSerial"""
        bot = FuniSerial(self.mock)
        long = 4.3
        bot.cal(FuniType.SET,FuniModeCalibration.CABLE,2,long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "cable", "id": 2, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")


    def test_cal_err_id_float(self):
        """Test de calibration du cable du FuniSerial avec un float comme id"""
        bot = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(TypeError, msg = "La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            bot.cal(FuniType.SET,FuniModeCalibration.CABLE,2.4,long)
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_cal_err_id_neg(self):
        """Test de calibration du cable du FuniSerial avec un négatif comme id"""
        bot = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(ValueError, msg = "La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            bot.cal(FuniType.SET,FuniModeCalibration.CABLE,-6,long)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_cal_err_long_none(self):
        """Test de calibration de FuniSerial avec une longueur None"""
        bot = FuniSerial(self.mock)
        long = None

        with self.assertRaises(ValueError, msg = "La présence de None comme longueur n'a pas levé d'exception de type ValueError") as re:
            bot.cal(FuniType.SET,FuniModeCalibration.CABLE,2,long)
        self.assertEqual(str(re.exception), "longueur est None")

    def test_cal_err_long_neg(self):
        """Test de calibration de FuniSerial avec une longueur négative"""
        bot = FuniSerial(self.mock)
        long = -4

        with self.assertRaises(ValueError, msg = "La présence d'un négatif comme longueur n'a pas levé d'exception de type ValueError") as re:
            bot.cal(FuniType.SET,FuniModeCalibration.CABLE,2,long)
        self.assertEqual(str(re.exception), "longueur est inférieure à zéro")

    def test_cal_get(self):
        """Test de calibration du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        long = 2.5
        bot.cal(FuniType.GET,FuniModeCalibration.CABLE,2,long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "get", "args": {{"mode": "cable", "id": 2, "long": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        long = 2.5

        with self.assertRaises(TypeError, msg = "La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.cal(FuniModeDeplacement.START,FuniModeCalibration.CABLE,2,long)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

