from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur, Poteau


class TestsPoteau(unittest.TestCase):

    def test_repr(self):
        position_pole = Vecteur(10, 2, 4)
        position_accroche = Vecteur(0, 0, 1)
        nom = "poteau_test"
        poteau = Poteau(nom="poteau_test",
                        position_pole=position_pole, position_accroche=position_accroche)
        self.assertTrue(poteau.__repr__(
        ) == "Poteau[-1:poteau_test](10;2;4)(0;0;1)", msg=f"__repr__() donne: {poteau.__repr__()}")

class TestVecteur(unittest.TestCase):

    def test_repr(self):
        VecteurTest = Vecteur(3,-2,7)
        self.assertTrue(VecteurTest.__repr__()== "(3;-2;7)",msg=f"__repr__() donne: {VecteurTest.__repr__()}")
