from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur, Poteau
from funibot_api.funibot_json_serial import FuniSerial
from tests.mock_serial import MockSerial


class TestsPoteau(unittest.TestCase):

    def test_repr(self):
        position_pole = Vecteur(10, 2, 4)
        position_accroche = Vecteur(0, 0, 1)
        nom = "poteau_test"
        poteau = Poteau(nom="poteau_test",
                        position_pole=position_pole, position_accroche=position_accroche)
        self.assertTrue(poteau.__repr__(
        ) == "Poteau[-1:poteau_test](10;2;4)(0;0;1)", msg=f"__repr__() donne: {poteau.__repr__()}")

    def test_initialiser_poteau(self):
        mock = MockSerial()
        serial = FuniSerial(mock)
        poteau = Poteau(nom="test_init")
        poteau.init_poteau(12, serial)