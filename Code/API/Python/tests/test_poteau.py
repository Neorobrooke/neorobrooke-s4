from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur, Poteau
from funibot_api.funibot_json_serial import FuniSerial
from tests.mock_serial import MockSerial, MockType


class TestsPoteau(unittest.TestCase):

    def test_repr(self):
        position_pole = Vecteur(10, 2, 4)
        position_accroche = Vecteur(0, 0, 1)
        nom = "poteau_test"
        poteau = Poteau(nom="poteau_test",
                        position_pole=position_pole, position_accroche=position_accroche)
        self.assertTrue(repr(poteau
                             ) == "Poteau[-1:poteau_test](10;2;4)(0;0;1)", msg=f"__repr__() donne: {poteau.__repr__()}")

    def test_initialiser_poteau_id_positif(self):
        mock = MockSerial(MockType.CLI)
        serial = FuniSerial(mock)
        poteau = Poteau(nom="test_init_id_positif")
        poteau.init_poteau(12, serial)

        self.assertEqual(poteau.id, 12)
        self.assertEqual(mock.requete, b'{"comm": "pot", "type": "set", "args": {"id": 12, "pos_x": 0, "pos_y": 0, "pos_z": 0}}')

    def test_initialiser_poteau_id_negatif(self):
        mock = MockSerial(MockType.CLI)
        serial = FuniSerial(mock)
        poteau = Poteau(nom="test_init_id_negatif")
        
        with self.assertRaises(ValueError, msg="ID de valeur négative acceptée"):
            poteau.init_poteau(-12, serial)

    def test_initialiser_poteau_id_reel(self):
        mock = MockSerial(MockType.CLI)
        serial = FuniSerial(mock)
        poteau = Poteau(nom="test_init_id_reel")

        with self.assertRaises(TypeError, msg="ID de valeur réelle acceptée"):
            poteau.init_poteau(1.3, serial) #type: ignore

    def test_initialiser_poteau_id_str(self):
        mock = MockSerial(MockType.CLI)
        serial = FuniSerial(mock)
        poteau = Poteau(nom="test_init_id_str")

        with self.assertRaises(TypeError, msg="ID sous forme de str accepté"):
            poteau.init_poteau("test_id_str", serial) #type: ignore