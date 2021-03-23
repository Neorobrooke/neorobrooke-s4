from __future__ import annotations
import unittest
from funibot_api.funilib import JamaisInitialise, Vecteur, Poteau
from funibot_api.funibot_json_serial import FuniSerial
from tests.mock_serial import DualMockSerial, MockSerial, MockType


class TestsPoteau(unittest.TestCase):
    """Tests sur la classe Poteau de funibot_api"""

    def setUp(self) -> None:
        """Préparation commune aux différents tests"""
        self.mock = MockSerial(MockType.TEST)
        self.serial = FuniSerial(self.mock)

        self.emock = MockSerial(MockType.TEST)
        self.dmock = DualMockSerial(
            canal_lecture=self.mock, canal_ecriture=self.emock)
        self.dserial = FuniSerial(self.dmock)

        self.index_poteau = 0

        return super().setUp()

    def test_repr(self):
        """Test de représentation d'un Poteau"""
        poteau = Poteau(nom="poteau_test",
                        position_pole=Vecteur(10, 2, 4), position_accroche=Vecteur(0, 0, 1))
        self.assertEqual(repr(poteau
                              ), "Poteau[-1:poteau_test](10;2;4)(0;0;1)", msg=f"__repr__() donne: {repr(poteau)}")

    def test_initialiser_poteau_id_positif(self):
        """Test d'initialisation de Poteau avec un ID positif"""
        poteau = Poteau(nom="test_init_id_positif")
        poteau.init_poteau(124, self.serial)

        self.assertEqual(poteau.id, 124)
        self.assertEqual(
            self.mock.requete, b'{"comm": "pot", "type": "set", "args": {"id": 124, "pos_x": 0, "pos_y": 0, "pos_z": 0}}')

    def test_initialiser_poteau_id_negatif(self):
        """Test d'initialisation de Poteau avec un ID négatif"""
        poteau = Poteau(nom="test_init_id_negatif")

        with self.assertRaises(ValueError, msg="ID de valeur négative acceptée") as re:
            poteau.init_poteau(-12, self.serial)

        self.assertEqual(str(re.exception), "id est inférieur à 0")

    def test_initialiser_poteau_id_reel(self):
        """Test d'initialisation de Poteau avec un ID réel"""
        poteau = Poteau(nom="test_init_id_reel")

        with self.assertRaises(TypeError, msg="ID de valeur réelle acceptée") as re:
            poteau.init_poteau(1.3, self.serial)  # type: ignore

        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_initialiser_poteau_id_str(self):
        """Test d'initialisation de Poteau avec un ID qui est une str"""
        poteau = Poteau(nom="test_init_id_str")

        with self.assertRaises(TypeError, msg="ID sous forme de str accepté") as re:
            poteau.init_poteau("test_id_str", self.serial)  # type: ignore

        self.assertEqual(str(re.exception), "id n'est pas un entier")

    def test_longueur_cable_pas_init(self):
        """Test d'obtention de longueur du câble avant initialisation"""
        poteau = Poteau(nom="test_longueur_cable_pas_init")

        with self.assertRaises(JamaisInitialise) as re:
            poteau.longueur_cable

        self.assertEqual(str(re.exception), str(
            JamaisInitialise(poteau=poteau, message="longueur_cable")))

    def test_longueur_cable(self):
        """Test d'obtention de longueur du câble"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.dserial)

        longueur_test = 931
        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "cal", "type": "ack", "args": {{"mode": "cable", "id": {self.index_poteau}, "long": {longueur_test}}}}}', 'utf8')

        self.assertEqual(poteau.longueur_cable, longueur_test,
                         msg="longueur_cable n'est pas bonne")

    def test_longueur_cable_exception(self):
        """Test d'obtention de longueur d'un câble avec un id négatif pour tester la remontée d'exceptions"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.serial)

        # On change l'id pour que 'cal' lance une exception
        poteau.id = -1

        # L'exception devrait être retransmise et garder son type (ValueError)
        with self.assertRaises(ValueError) as re:
            poteau.longueur_cable

        self.assertEqual(str(re.exception), "id est inférieur à 0",
                         msg="L'exception ValueError dans 'cal' n'a pas été retransmise.")

    def test_set_longueur_cable_pas_init(self):
        """Test de calibration de longueur du câble avant initialisation"""
        poteau = Poteau(nom="test_longueur_cable_pas_init")

        with self.assertRaises(JamaisInitialise) as re:
            poteau.longueur_cable = 435

        self.assertEqual(str(re.exception), str(JamaisInitialise(
            poteau=poteau, message="longueur_cable.setter")))

    def test_set_longueur_cable(self):
        """Test de calibration de longueur du câble"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.serial)

        longueur_test = 76223
        message_attendu = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "cable", "id": {self.index_poteau}, "long": {longueur_test}}}}}', 'utf8')

        poteau.longueur_cable = longueur_test
        message_obtenu = self.mock.requete
        self.assertEqual(message_obtenu, message_attendu,
                         msg="Changer la longueur du câble (calibration) a échoué")

    def test_set_longueur_cable_negative(self):
        """Test de calibration de longueur du câble négative"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.serial)

        longueur_test = -4672

        with self.assertRaises(ValueError) as re:
            poteau.longueur_cable = longueur_test

        self.assertEqual(str(re.exception), "longueur est inférieure à zéro")

    def test_set_longueur_cable_float(self):
        """Test de calibration de longueur du câble entière"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.serial)

        longueur_test = 467.43
        message_attendu = bytes(
            f'{{"comm": "cal", "type": "set", "args": {{"mode": "cable", "id": {self.index_poteau}, "long": {longueur_test}}}}}', 'utf8')

        poteau.longueur_cable = longueur_test
        message_obtenu = self.mock.requete
        self.assertEqual(message_obtenu, message_attendu,
                         msg="Changer la longueur du câble (calibration) a échoué avec une valeur réelle")

    def test_set_longueur_cable_none(self):
        """Test de calibration de longueur du câble avec None"""
        poteau = Poteau(nom="test_longueur_cable")
        poteau.init_poteau(self.index_poteau, self.serial)

        longueur_test = None

        with self.assertRaises(ValueError) as re:
            poteau.longueur_cable = longueur_test  # type: ignore

        self.assertEqual(str(re.exception), "longueur est None")

    def test_courant_moteur_pas_init(self):
        """Test d'obtention de courant du moteur avant initialisation"""
        poteau = Poteau(nom="test_courant_moteur_pas_init")

        with self.assertRaises(JamaisInitialise) as re:
            poteau.courant_moteur

        self.assertEqual(str(re.exception), str(
            JamaisInitialise(poteau=poteau, message="courant_moteur")))

    def test_couple_moteur_pas_init(self):
        """Test d'obtention de couple du moteur avant initialisation"""
        poteau = Poteau(nom="test_courant_moteur_pas_init")

        with self.assertRaises(JamaisInitialise) as re:
            poteau.couple_moteur

        self.assertEqual(str(re.exception), str(
            JamaisInitialise(poteau=poteau, message="couple_moteur")))

    def test_repr_cable(self):
        """Test de représentation d'un Câble"""
        poteau = Poteau(nom="poteau_test")
        poteau.init_poteau(self.index_poteau, self.dserial)

        longueur_test = 467.43
        self.dmock.lecture.reponse = bytes(
            f'{{"comm": "cal", "type": "ack", "args": {{"mode": "cable", "id": {self.index_poteau}, "long": {longueur_test}}}}}', 'utf8')

        poteau.longueur_cable = longueur_test

        self.assertEqual(poteau.repr_cable(
        ), "Câble[0:poteau_test] -> 467.43", msg=f"La représentation du câble donne: {poteau.repr_cable()}")
