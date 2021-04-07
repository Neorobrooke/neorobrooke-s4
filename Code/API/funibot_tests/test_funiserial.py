from __future__ import annotations
from typing import Tuple, List

from funibot_api.funiserial import FUNI_ERREUR_MAJ, FuniErreur, eFuniModeCalibration, eFuniModeDeplacement, FuniSerial, eFuniModeMoteur, eFuniType, eFuniErreur
from funibot_api.funimock import MockSerial, eMockType, DualMockSerial
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
        self.mock = MockSerial(eMockType.TEST)
        self.emock = MockSerial(eMockType.TEST)
        self.dmock = DualMockSerial(
            canal_lecture=self.mock, canal_ecriture=self.emock)

    def test_repr(self):
        """Test de représentation d'un FuniSerial"""
        serial = FuniSerial(self.mock)

        self.assertEqual(repr(
            serial), "Mock", msg=f"La représentation du FuniSerial est {repr(serial)} au lieu de Mock")

    def test_pot(self):
        """Test du poteau du FuniSerial"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pot(eFuniType.SET, 0, position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "set", "args": {{"id": 0, "pos_x": {position[0]}, "pos_y": {position[1]}, "pos_z": {position[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_id_float(self):
        """Test du poteau du FuniSerial avec un float comme id"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)

        with self.assertRaises(TypeError, msg="La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            serial.pot(eFuniType.SET, 1.4, position)  # type: ignore
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_pot_err_id_neg(self):
        """Test du poteau du FuniSerial avec un négatif comme id"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            serial.pot(eFuniType.SET, -2, position)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_pot_err_pos_none(self):
        """Test du poteau du FuniSerial avec une position None"""
        serial = FuniSerial(self.mock)
        position = None

        with self.assertRaises(ValueError, msg="La présence de None comme position n'a pas levé d'exception de type ValueError") as re:
            serial.pot(eFuniType.SET, 2, position)
        self.assertEqual(str(re.exception), "position est None")

    def test_pot_get(self):
        """Test du poteau du FuniSerial avec get"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pot(eFuniType.GET, 0, position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "get", "args": {{"id": 0, "pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_ack(self):
        """Test du poteau du FuniSerial avec ack"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pot(eFuniType.ACK, 0, position)

        validation_requete = bytes(
            f'{{"comm": "pot", "type": "ack", "args": {{"id": 0, "pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le poteau avec ack est {validation_requete} au lieu de {self.mock.requete}")

    def test_pot_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)
        position = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.pot(eFuniModeDeplacement.START, 2, position)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_cal_sol(self):
        """Test de calibration du sol du FuniSerial"""
        serial = FuniSerial(self.mock)
        long = 4.3
        serial.cal(eFuniType.SET, eFuniModeCalibration.SOL, 0, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "sol", "id": null, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration du sol est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_cable(self):
        """Test de calibration des cables du FuniSerial"""
        serial = FuniSerial(self.mock)
        long = 4.3
        serial.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "cable", "id": 2, "long": {long}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_ack(self):
        """Test de calibration des cables avec ack du FuniSerial"""
        serial = FuniSerial(self.mock)
        long = 4.3
        serial.cal(eFuniType.ACK, eFuniModeCalibration.CABLE, 2, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "ack", "args": {{"mode": "cable", "id": 2, "long": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables avec ack est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_err_id_float(self):
        """Test de calibration du cable du FuniSerial avec un float comme id"""
        serial = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(TypeError, msg="La présence d'un float comme id n'a pas levé d'exception de type TypeError") as re:
            serial.cal(eFuniType.SET, eFuniModeCalibration.CABLE,
                       2.4, long)  # type: ignore
        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_cal_err_id_neg(self):
        """Test de calibration du cable du FuniSerial avec un négatif comme id"""
        serial = FuniSerial(self.mock)
        long = 4.3

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme id n'a pas levé d'exception de type ValueError") as re:
            serial.cal(eFuniType.SET, eFuniModeCalibration.CABLE, -6, long)
        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_cal_err_long_none(self):
        """Test de calibration de FuniSerial avec une longueur None"""
        serial = FuniSerial(self.mock)
        long = None

        with self.assertRaises(ValueError, msg="La présence de None comme longueur n'a pas levé d'exception de type ValueError") as re:
            serial.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "longueur est None")

    def test_cal_err_long_neg(self):
        """Test de calibration de FuniSerial avec une longueur négative"""
        serial = FuniSerial(self.mock)
        long = -4

        with self.assertRaises(ValueError, msg="La présence d'un négatif comme longueur n'a pas levé d'exception de type ValueError") as re:
            serial.cal(eFuniType.SET, eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "longueur est inférieure à zéro")

    def test_cal_get(self):
        """Test de calibration du FuniSerial avec get"""
        serial = FuniSerial(self.mock)
        long = 2.5
        serial.cal(eFuniType.GET, eFuniModeCalibration.CABLE, 2, long)

        validation_requete = bytes(
            f'{{"comm": "cal", "type": "get", "args": {{"mode": "cable", "id": 2, "long": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La calibration des cables est {validation_requete} au lieu de {self.mock.requete}")

    def test_cal_err_type(self):
        """Test du poteau du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)
        long = 2.5

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.cal(eFuniModeDeplacement.START,  # type: ignore
                       eFuniModeCalibration.CABLE, 2, long)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_pos(self):
        """Test de la position du FuniSerial"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pos(eFuniType.SET, position)

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "set", "args": {{"pos_x": {position[0]}, "pos_y": {position[1]}, "pos_z": {position[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La position est {validation_requete} au lieu de {self.mock.requete}")

    def test_pos_ack(self):
        """Test de la position avec ack du FuniSerial"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pos(eFuniType.ACK, position)

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "ack", "args": {{"pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La position avec ack est {validation_requete} au lieu de {self.mock.requete}")

    def test_pos_err_none(self):
        """Test de position du FuniSerial avec un None"""
        serial = FuniSerial(self.mock)
        position = None

        with self.assertRaises(ValueError, msg="La présence de None comme position n'a pas levé d'exception de type ValueError") as re:
            serial.pos(eFuniType.SET, position)
        self.assertEqual(str(re.exception), "position est None")

    def test_pos_get(self):
        """Test de position du FuniSerial avec get"""
        serial = FuniSerial(self.mock)
        position = (3, 1.2, 8)
        serial.pos(eFuniType.GET, position)

        validation_requete = bytes(
            f'{{"comm": "pos", "type": "get", "args": {{"pos_x": null, "pos_y": null, "pos_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"La position est {validation_requete} au lieu de {self.mock.requete}")

    def test_pos_err_type(self):
        """Test de position du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)
        position = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.pos(eFuniModeDeplacement.START, position)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_dep_start(self):
        """Test de déplacement du FuniSerial avec start"""
        serial = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        serial.dep(eFuniType.SET, eFuniModeDeplacement.START, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "start", "axe_x": {direction[0]}, "axe_y": {direction[1]}, "axe_z": {direction[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec start est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep_start_ack(self):
        """Test de déplacement avec ack du FuniSerial avec start"""
        serial = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        serial.dep(eFuniType.ACK, eFuniModeDeplacement.START, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "ack", "args": {{"mode": "start", "axe_x": null, "axe_y": null, "axe_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec start et ack est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep_dist(self):
        """Test de déplacement du FuniSerial avec distance"""
        serial = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        serial.dep(eFuniType.SET, eFuniModeDeplacement.DISTANCE, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "distance", "axe_x": {direction[0]}, "axe_y": {direction[1]}, "axe_z": {direction[2]}}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec distance est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep__err_dir_none(self):
        """Test de déplacement du FuniSerial avec une direction None"""
        serial = FuniSerial(self.mock)
        direction = None

        with self.assertRaises(ValueError, msg="La présence de None comme direction n'a pas levé d'exception de type ValueError") as re:
            serial.dep(eFuniType.SET, eFuniModeDeplacement.DISTANCE, direction)
        self.assertEqual(str(re.exception), "direction est None")

    def test_dep_stop(self):
        """Test de déplacement du FuniSerial en mode stop"""
        serial = FuniSerial(self.mock)
        direction = (3, 1.2, 8)
        serial.dep(eFuniType.SET, eFuniModeDeplacement.STOP, direction)

        validation_requete = bytes(
            f'{{"comm": "dep", "type": "set", "args": {{"mode": "stop", "axe_x": null, "axe_y": null, "axe_z": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le déplacement avec stop est {validation_requete} au lieu de {self.mock.requete}")

    def test_dep__err_get(self):
        """Test de déplacement du FuniSerial avec get"""
        serial = FuniSerial(self.mock)
        direction = (3, 4, 1)

        with self.assertRaises(ValueError, msg="La présence du type get n'a pas levé d'exception de type ValueError") as re:
            serial.dep(eFuniType.GET, eFuniModeDeplacement.DISTANCE, direction)
        self.assertEqual(str(re.exception), "GET n'est pas supporté")

    def test_dep_err_type(self):
        """Test de déplacement du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)
        deplacement = None

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.dep(eFuniModeDeplacement.START,  # type: ignore
                       eFuniModeDeplacement.DISTANCE, deplacement)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_err_get(self):
        """Test des erreurs avec get du FuniSerial"""
        serial = FuniSerial(self.dmock)

        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 1, "maj": true, "t": 4252452, "err_sup": 0}}}}', 'utf8')
        validation_requete = bytes(
            f'{{"comm": "err", "type": "get", "args": {{"id": null, "maj": null, "t": null, "err_sup": null}}}}', 'utf8')

        reponse = serial.err(eFuniType.GET)

        self.assertEqual(len(reponse), 1)
        erreur = reponse[0]

        self.assertIs(erreur.erreur, eFuniErreur.ADD_POLE_DEPASSEMENT)
        self.assertEqual(erreur.id, eFuniErreur.ADD_POLE_DEPASSEMENT.value)
        self.assertEqual(erreur.t, 4252452)

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec get est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_get_multiple(self):
        """Test d'obention de plusieurs erreurs avec get de FuniSerial"""
        multimock = DualMockSerial(MockSerial(
            eMockType.MULTI_TEST), MockSerial(eMockType.MULTI_TEST))
        serial = FuniSerial(multimock)

        erreurs: List[FuniErreur] = []
        erreurs.append(FuniErreur(1, 24235, True))
        erreurs.append(FuniErreur(14, 3435534, False))
        erreurs.append(FuniErreur(43, 245643643634, True))

        total = len(erreurs) - 1

        for num, item in enumerate(erreurs):
            multimock.lecture.reponses.append(bytes(
                f'{{"comm": "err", "type": "ack", "args": {{"id": {item.id}, "maj": {str(item.maj).lower()}, "t": {item.t}, "err_sup": {total - num}}}}}', 'utf8'))

        validation_requete = bytes(
            f'{{"comm": "err", "type": "get", "args": {{"id": null, "maj": null, "t": null, "err_sup": null}}}}', 'utf8')

        reponse = serial.err(eFuniType.GET)

        self.assertEqual(len(reponse), len(erreurs), msg=f"Le nombre d'erreurs est de {len(reponse)} au lieu de {len(erreurs)}")
        
        for index, erreur in enumerate(reponse):
            attendu = erreurs[index]

            self.assertIs(erreur.erreur, attendu.erreur, msg=f"Les erreurs ne concordent pas: {erreur.erreur.name} au lieu de {attendu.erreur.name}")
            self.assertEqual(erreur.id, attendu.id, msg=f"Les id ne concordent pas: {erreur.id} au lieu de {attendu.id}")
            self.assertEqual(erreur.t, attendu.t, msg=f"Les temps ne concordent pas: {erreur.t} au lieu de {attendu.t}")
            self.assertEqual(erreur.maj, attendu.maj, msg=f"Les majeures ne concordent pas: {erreur.maj} au lieu de {attendu.maj}")

            self.assertEqual(multimock.ecriture.requetes[index], validation_requete,
                            msg=f"La requête est {multimock.ecriture.requetes[index]} au lieu de {validation_requete}")

    def test_err_set(self):
        """Test des erreurs avec set du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="Le FuniType set n'a pas levé d'exception de type ValueError") as re:
            serial.err(eFuniType.SET, 2, 0, 0)
        self.assertEqual(str(re.exception), "SET n'est pas supporté")

    def test_err_funitype(self):
        """Test des erreurs sans FuniType du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le FuniType set n'a pas levé d'exception de type TypeError") as re:
            serial.err(eFuniModeDeplacement.START, 2, 0, 0)  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_err_ack(self):
        """Test des erreurs avec ack du FuniSerial"""
        serial = FuniSerial(self.dmock)

        serial.err(eFuniType.ACK, 1, 4252452, 0)

        validation_requete = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 1, "maj": {str(FUNI_ERREUR_MAJ[1]).lower()}, "t": 4252452, "err_sup": 0}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec ack est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_eFuniErreur(self):
        """Test des erreurs du FuniSerial avec eFuniErreur"""
        serial = FuniSerial(self.dmock)

        serial.err(
            eFuniType.ACK, eFuniErreur.DEPLACEMENT_DIRECTIONNEL_ERREUR_MAJEURE, 4252452, 0)

        validation_requete = bytes(
            f'{{"comm": "err", "type": "ack", "args": {{"id": 11, "maj": {str(FUNI_ERREUR_MAJ[1]).lower()}, "t": 4252452, "err_sup": 0}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"L'erreur avec ack et avec eFuniErreur est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_err_code_float(self):
        """Test des erreurs avec code float du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le float comme code n'a pas levé d'exception de type TypeError") as re:
            serial.err(eFuniType.ACK, 0.3, 4252452, 0)  # type: ignore
        self.assertEqual(str(re.exception),
                         "code n'est pas une eFuniErreur ou un entier")

    def test_err_code_neg(self):
        """Test des erreurs avec code négatif du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="Le code négatif n'a pas levé d'exception de type ValueError") as re:
            serial.err(eFuniType.ACK, -6, 4252452, 0)
        self.assertEqual(str(re.exception),
                         "code est un entier négatif, il devrait être positif")

    def test_err_temps_float(self):
        """Test des erreurs avec temps float du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="Le temps en float n'a pas levé d'exception de type TypeError") as re:
            serial.err(eFuniType.ACK, 6, 5.76, 0)  # type: ignore
        self.assertEqual(str(re.exception), "temps n'est pas un entier")

    def test_err_errsup_float(self):
        """Test des erreurs avec err_sup float du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(TypeError, msg="L'err_sup en float n'a pas levé d'exception de type TypeError") as re:
            serial.err(eFuniType.ACK, 6, 345, 0.54)  # type: ignore
        self.assertEqual(str(re.exception), "err_sup n'est pas un entier")

    def test_err_errsup_neg(self):
        """Test des erreurs avec err_sup négatif du FuniSerial"""
        serial = FuniSerial(self.dmock)

        with self.assertRaises(ValueError, msg="L'err_sup en négatif n'a pas levé d'exception de type ValueError") as re:
            serial.err(eFuniType.ACK, 6, 345, -5)
        self.assertEqual(str(re.exception), "err_sup est négatif")

    def test_log_get(self):
        """Test de log du FuniSerial avec get"""
        serial = FuniSerial(self.mock)

        serial.log(eFuniType.GET, "allo")

        validation_requete = bytes(
            f'{{"comm": "log", "type": "get", "args": {{"msg": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Le log avec get est {validation_requete} au lieu de {self.mock.requete}")

    def test_log_err_set(self):
        """Test de log du FuniSerial avec set"""
        serial = FuniSerial(self.mock)

        with self.assertRaises(ValueError, msg="La présence du type set n'a pas levé d'exception de type ValueError") as re:
            serial.log(eFuniType.SET, "allo")
        self.assertEqual(str(re.exception), "SET n'est pas supporté")

    def test_log_err_type(self):
        """Test de log du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.log(eFuniModeCalibration.SOL, "allo")  # type: ignore
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_log_ack(self):
        """Test de log du FuniSerial avec ack"""
        serial = FuniSerial(self.dmock)

        serial.log(eFuniType.ACK, "allo")

        validation_requete = bytes(
            f'{{"comm": "log", "type": "ack", "args": {{"msg": "allo"}}}}', 'utf8')

        self.assertEqual(self.dmock.ecriture.requete, validation_requete,
                         msg=f"Le log avec ack est {validation_requete} au lieu de {self.dmock.ecriture.requete}")

    def test_mot_set(self):
        """Test des moteurs du FuniSerial avec SET"""
        serial = FuniSerial(self.mock)
        serial.mot(eFuniType.SET, eFuniModeMoteur.ON)

        validation_requete = bytes(
            f'{{"comm": "mot", "type": "set", "args": {{"mode": "on"}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Les moteurs avec set sont {validation_requete} au lieu de {self.mock.requete}")

    def test_mot_get(self):
        """Test des moteurs du FuniSerial avec GET"""
        serial = FuniSerial(self.mock)
        serial.mot(eFuniType.GET, eFuniModeMoteur.ON)

        validation_requete = bytes(
            f'{{"comm": "mot", "type": "get", "args": {{"mode": null}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Les moteurs avec get sont {validation_requete} au lieu de {self.mock.requete}")

    def test_mot_err_type(self):
        """Test des moteurs du FuniSerial avec un type pas FuniType"""
        serial = FuniSerial(self.mock)

        with self.assertRaises(TypeError, msg="La présence d'un type n'étant pas un Funitype n'a pas levé d'exception de type TypeError") as re:
            serial.mot(eFuniModeDeplacement.START,  # type: ignore
                       eFuniModeMoteur.OFF)
        self.assertEqual(str(re.exception), "type n'est pas un FuniType")

    def test_mot_ack(self):
        """Test des moteurs du FuniSerial avec un ack"""
        serial = FuniSerial(self.mock)
        serial.mot(eFuniType.ACK, eFuniModeMoteur.ON)

        validation_requete = bytes(
            f'{{"comm": "mot", "type": "ack", "args": {{"mode": "on"}}}}', 'utf8')

        self.assertEqual(self.mock.requete, validation_requete,
                         msg=f"Les moteurs avec ack sont {validation_requete} au lieu de {self.mock.requete}")

    def test_mot_ack_mode_none(self):
        """Test des moteurs du FuniSerial avec un ack et mode None"""
        serial = FuniSerial(self.mock)

        with self.assertRaises(ValueError, msg="La présence de ack avec un mode None n'a pas levé d'exception de type ValueError") as re:
            serial.mot(eFuniType.ACK)
        self.assertEqual(str(re.exception), "mode est None")
