from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur


class TestVecteur(unittest.TestCase):

    def test_repr(self):
        VecteurTest = Vecteur(3, -2, 7)
        self.assertTrue(VecteurTest.__repr__() == "(3;-2;7)",
                        msg=f"__repr__() donne: {VecteurTest.__repr__()}")
