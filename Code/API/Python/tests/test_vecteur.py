from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur

class TestVecteur(unittest.TestCase):

    def test_repr(self):
        """ Test d'un vecteur pour voir s'il se représente bien"""
        VecteurTest = Vecteur(3,-2,7)
        self.assertTrue(repr(VecteurTest)== "(3;-2;7)",msg=f"__repr__() donne: {VecteurTest.__repr__()}")
    
    def test_add(self):
        VecteurBase = Vecteur(2,7,-4)
        VecteurAdd = Vecteur(-7,2,10)
        self.assertTrue(VecteurBase + VecteurAdd == Vecteur(-5,9,6), msg=f"__add__() donne: {VecteurBase + VecteurAdd}")

    def test_add_err(self):
        VecteurBase = Vecteur(5,-2,13)
        Reel = 8
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            VecteurBase + Reel 