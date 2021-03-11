from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur

class TestVecteur(unittest.TestCase):

    def test_repr(self):
        """Test d'un vecteur pour voir s'il se représente bien"""
        VecteurTest = Vecteur(3,-2,7)
        self.assertTrue(repr(VecteurTest)== "(3;-2;7)",msg=f"__repr__() donne: {VecteurTest.__repr__()}")
    
    def test_add(self):
        """Test d'addition de deux vecteurs"""
        VecteurBase = Vecteur(2,7,-4)
        VecteurAdd = Vecteur(-7,2,10)
        self.assertTrue(VecteurBase + VecteurAdd == Vecteur(-5,9,6), msg=f"__add__() donne: {VecteurBase + VecteurAdd}")

    def test_add_null(self):
        """Test d'addition d'un vecteur null avec un vecteur ayant des valeurs"""
        self.assertTrue(Vecteur() + Vecteur(2,5,8.5) == Vecteur(2,5,8.5),  msg=f"__add__() donne: {Vecteur() + Vecteur(2,5,8.5)}")
    
    def test_add_err(self):
        """Test d'addition d'un nombre réel à un vecteur"""
        VecteurBase = Vecteur(5,-2,13)
        Reel = 8
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            VecteurBase + Reel 

    def test_sub(self):
        """ Test soustraction de deux vecteurs"""
        VecteurBase = Vecteur(2,7,-4)
        VecteurSub = Vecteur(-7,2,10)
        self.assertTrue(VecteurBase - VecteurSub == Vecteur(9,5,-14), msg=f"__sub__() donne: {VecteurBase - VecteurSub}")

    def test_sub_null(self):
        """ Soustraction par un vecteur null"""
        self.assertTrue(Vecteur(2,5,8.5) - Vecteur() == Vecteur(2,5,8.5),  msg=f"__sub__() donne: {Vecteur(2,5,8.5)-Vecteur()}")
    
    def test_sub_err(self):
        """ Test de soustraction d'un nombre réel à un vecteur"""
        VecteurBase = Vecteur(5,-2,13)
        Reel = 8
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            VecteurBase - Reel

    def test_mul_err(self):
        """ Test multiplication de deux vecteurs"""
        VecteurBase = Vecteur(2,7,-4)
        VecteurMul = Vecteur(-7,2,10)
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            VecteurBase * VecteurMul

    def test_mul_null(self):
        """ Test de multiplication par zéro"""
        self.assertTrue(Vecteur(2,5,8.5) * 0 == Vecteur(),  msg=f"__mul__() donne: {Vecteur(2,5,8.5)*0}")
    
    def test_mul(self):
        """ Test de multiplication d'un nombre réel à un vecteur"""
        VecteurBase = Vecteur(5,-2,13)
        Reel = 8
        self.assertTrue(VecteurBase * Reel == Vecteur(40,-16,104), msg=f"__mul__() donne: {VecteurBase * Reel}")