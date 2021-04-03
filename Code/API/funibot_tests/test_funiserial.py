from __future__ import annotations
from typing import Tuple

from funibot_api.funiserial import FUNI_ERREUR_MAJ, FuniErreur, eFuniModeCalibration, eFuniModeDeplacement, FuniSerial, eFuniType, eFuniErreur
from funibot_api.mock_serial import MockSerial, MockType, DualMockSerial
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
        self.dmock = DualMockSerial(
            canal_lecture=self.mock, canal_ecriture=self.emock)

    def test_repr(self):
        """Test de représentation d'un FuniSerial"""
        bot = FuniSerial(self.mock)

        self.assertEqual(repr(
            bot), "Mock", msg=f"La représentation du FuniSerial est {repr(bot)} au lieu de Mock")

    def test_pot(self):
        """Test du poteau du FuniSerial"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        bot.pot(eFuniType.SET, 0, position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "set", "args": {{"id": 0, "pos_x": {position[0]}, "pos_y": {position[1]}, "pos_z": {position[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_id_float(self):
        """Test du poteau du FuniSerial avec un float comme id"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)

        with self.assertRaises(TypeError, msg="La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            bot.pot(eFuniType.SET, 1.4, position)  # type: ignore
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_pot_err_id_neg(self):
        """Test du poteau du FuniSerial avec un négatif comme id"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            bot.pot(eFuniType.SET, -2, position)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_pot_err_pos_none(self):
        """Test du poteau du FuniSerial avec une position None"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(ValueError, msg="La présence de None comme position n'a pas levé d'exception de type ValueError") as re:
            bot.pot(eFuniType.SET, 2, position)
        self.assertEqual(str(re.exception), "position est None")

    def test_pot_get(self):
        """Test du poteau du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        bot.pot(eFuniType.GET, 0, position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "get", "args": {{"id": 0, "pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.pot(eFuniModeDeplacement.START, 2, position)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_cal_sol(self):
        """Test de calibration du sol du FuniSerial"""
        bot = FuniSerial(self.mock)
        long = 4.3
        bot.cal(eFuniType.SET, eFuniModeCalibration.SOL, 0, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "sol", "id": null, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration du sol est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_cable(self):
        """Test de calibration des cables du FuniSerial"""
        bot = FuniSerial(self.mock)
        long = 4.3
        bot.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "cable", "id": 2, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_err_id_float(self):
        """Test de calibration du cable du FuniSerial avec un float comme id"""
        bot = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(TypeError, msg="La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            bot.cal(eFuniType.SET, eFuniModeCalibration.CABLE,
                    2.4, long)  # type: ignore
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_cal_err_id_neg(self):
        """Test de calibration du cable du FuniSerial avec un négatif comme id"""
        bot = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            bot.cal(eFuniType.SET, eFuniModeCalibration.CABLE, -6, long)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_cal_err_long_none(self):
        """Test de calibration de FuniSerial avec une longueur None"""
        bot = FuniSerial(self.mock)
        long = None

        with self.assertRaises(ValueError, msg="La présence de None comme longueur n'a pas levé d'exception de type ValueError") as re:
            bot.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "longueur est None")

    def test_cal_err_long_neg(self):
        """Test de calibration de FuniSerial avec une longueur négative"""
        bot = FuniSerial(self.mock)
        long = -4

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme longueur n'a pas levé d'exception de type ValueError") as re:
            bot.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "longueur est inférieure à zéro")

    def test_cal_get(self):
        """Test de calibration du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        long = 2.5
        bot.cal(eFuniType.GET, eFuniModeCalibration.CABLE, 2, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "get", "args": {{"mode": "cable", "id": 2, "long": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        long = 2.5

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.cal(eFuniModeDeplacement.START, # type: ignore
                    eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_pos(self):
        """Test de la position du FuniSerial"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        bot.pos(eFuniType.SET, position)

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "set", "args": {{"pos_x": {position[0]}, "pos_y": {position[1]}, "pos_z": {position[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La position est {validation_requete} au lieu de {self.mock.requete}")

    def test_pos_err_none(self):
        """Test de position du FuniSerial avec un None"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(ValueError, msg="La présence de None comme position n'a pas levé d'exception de type ValueError") as re:
            bot.pos(eFuniType.SET, position)
        self.assertEqual(str(re.exception), "position est None")

    def test_pos_get(self):
        """Test de position du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        bot.pos(eFuniType.GET, position)

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "get", "args": {{"pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La position est {validation_requete} au lieu de {self.mock.requete}")

    def test_pos_err_type(self):
        """Test de position du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        position = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.pos(eFuniModeDeplacement.START, position)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_dep_start(self):
        """Test de déplacement du FuniSerial avec start"""
        bot = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        bot.dep(eFuniType.SET, eFuniModeDeplacement.START, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "start", "axe_x": {direction[0]}, "axe_y": {direction[1]}, "axe_z": {direction[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec start est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep_dist(self):
        """Test de déplacement du FuniSerial avec distance"""
        bot = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        bot.dep(eFuniType.SET, eFuniModeDeplacement.DISTANCE, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "distance", "axe_x": {direction[0]}, "axe_y": {direction[1]}, "axe_z": {direction[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec distance est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep__err_dir_none(self):
        """Test de déplacement du FuniSerial avec une direction None"""
        bot = FuniSerial(self.mock)
        direction = None

        with self.assertRaises(ValueError, msg="La présence de None comme direction n'a pas levé d'exception de type ValueError") as re:
            bot.dep(eFuniType.SET, eFuniModeDeplacement.DISTANCE, direction)
        self.assertEqual(str(re.exception), "direction est None")

    def test_dep_stop(self):
        """Test de déplacement du FuniSerial en mode stop"""
        bot = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        bot.dep(eFuniType.SET, eFuniModeDeplacement.STOP, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "stop", "axe_x": null, "axe_y": null, "axe_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec stop est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep__err_get(self):
        """Test de déplacement du FuniSerial avec get"""
        bot = FuniSerial(self.mock)
        direction = (3, 4, 1)

        with self.assertRaises(ValueError, msg="La présence du type get n'a pas levé d'exception de type ValueError") as re:
            bot.dep(eFuniType.GET, eFuniModeDeplacement.DISTANCE, direction)
        self.assertEqual(str(re.exception), "GET n'est pas supporté")

    def test_dep_err_type(self):
        """Test de déplacement du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)
        deplacement = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.dep(eFuniModeDeplacement.START, # type: ignore
                    eFuniModeDeplacement.DISTANCE, deplacement)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_err_get(self):
        """Test des erreurs avec get du FuniSerial"""
        bot = FuniSerial(self.dmock)

        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 1, "maj": true, "t": 4252452, "err_sup": 0}}}}', 'utf8')
        validation_requete = bytes(
            f'{{"comm": "err", "type": "get", "args": {{"id": null, "maj": null, "t": null, "err_sup": null}}}}', 'utf8')

        reponse = bot.err(eFuniType.GET)

        self.assertEqual(len(reponse), 1)
        erreur = reponse[0]

        self.assertIs(erreur.erreur, eFuniErreur.ADD_POLE_DEPASSEMENT)
        self.assertEqual(erreur.id, eFuniErreur.ADD_POLE_DEPASSEMENT.value)
        self.assertEqual(erreur.t, 4252452)

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec get est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_set(self):
        """Test des erreurs avec set du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="Le FuniType set n'a pas levé d'exception de type ValueError") as re:
            bot.err(eFuniType.SET, 2, 0, 0)
        self.assertEqual(str(re.exception), "SET n'est pas supporté")

    def test_err_funitype(self):
        """Test des erreurs sans FuniType du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le FuniType set n'a pas levé d'exception de type TypeError") as re:
            bot.err(eFuniModeDeplacement.START, 2, 0, 0)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_err_ack(self):
        """Test des erreurs avec ack du FuniSerial"""
        bot = FuniSerial(self.dmock)

        bot.err(eFuniType.ACK, 1, 4252452, 0)

        validation_requete = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 1, "maj": {str(FUNI_ERREUR_MAJ[1]).lower()}, "t": 4252452, "err_sup": 0}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec ack est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_eFuniErreur(self):
        """Test des erreurs du FuniSerial avec eFuniErreur"""
        bot = FuniSerial(self.dmock)

        bot.err(
            eFuniType.ACK, eFuniErreur.DEPLACEMENT_DIRECTIONNEL_ERREUR_MAJEURE, 4252452, 0)

        validation_requete = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 11, "maj": {str(FUNI_ERREUR_MAJ[1]).lower()}, "t": 4252452, "err_sup": 0}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec ack et avec eFuniErreur est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_code_float(self):
        """Test des erreurs avec code float du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le float comme code n'a pas levé d'exception de type TypeError") as re:
            bot.err(eFuniType.ACK, 0.3, 4252452, 0)  # type: ignore
        self.assertEqual(str(re.exception),
                         "code n'est pas une eFuniErreur ou un entier")

    def test_err_code_neg(self):
        """Test des erreurs avec code négatif du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="Le code négatif n'a pas levé d'exception de type ValueError") as re:
            bot.err(eFuniType.ACK, -6, 4252452, 0)
        self.assertEqual(str(re.exception),
                         "code est un entier négatif, il devrait être positif")

    def test_err_temps_float(self):
        """Test des erreurs avec temps float du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le temps en float n'a pas levé d'exception de type TypeError") as re:
            bot.err(eFuniType.ACK, 6, 5.76, 0)  # type: ignore
        self.assertEqual(str(re.exception), "temps n'est pas un entier")

    def test_err_errsup_float(self):
        """Test des erreurs avec err_sup float du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="L'err_sup en float n'a pas levé d'exception de type TypeError") as re:
            bot.err(eFuniType.ACK, 6, 345, 0.54)  # type: ignore
        self.assertEqual(str(re.exception), "err_sup n'est pas un entier")

    def test_err_errsup_neg(self):
        """Test des erreurs avec err_sup négatif du FuniSerial"""
        bot = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="L'err_sup en négatif n'a pas levé d'exception de type ValueError") as re:
            bot.err(eFuniType.ACK, 6, 345, -5)
        self.assertEqual(str(re.exception), "err_sup est négatif")

    def test_log_get(self):
        """Test de log du FuniSerial avec get"""
        bot = FuniSerial(self.mock)

        bot.log(eFuniType.GET, "allo")

        validation_requete = bytes(
            f'{{"comm": "log", "type": "get", "args": {{"msg": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le log avec get est {validation_requete} au lieu de {self.mock.requete}")

    def test_log__err_set(self):
        """Test de log du FuniSerial avec set"""
        bot = FuniSerial(self.mock)

        with self.assertRaises(ValueError, msg="La présence du type set n'a pas levé d'exception de type ValueError") as re:
            bot.log(eFuniType.SET, "allo")
        self.assertEqual(str(re.exception), "SET n'est pas supporté")

    def test_log_err_type(self):
        """Test de log du FuniSerial avec un type pas FuniType"""
        bot = FuniSerial(self.mock)

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            bot.log(eFuniModeCalibration.SOL, "allo")  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_log_ack(self):
        """Test de log du FuniSerial avec ack"""
        bot = FuniSerial(self.dmock)

        bot.log(eFuniType.ACK, "allo")

        validation_requete = bytes(
            f'{{"comm": "log", "type": "ack", "args": {{"msg": "allo"}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"Le log avec ack est {validation_requete} au lieu de {self.dmock.ecriture.requete}")
