from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur

class TestVecteur(unittest.TestCase):
    """ Test sur la classe Vecteur"""

    def test_repr(self):
        """Test d'un vecteur pour voir s'il se représente bien"""
        vecteur_test = Vecteur(3,-2,7)
        self.assertTrue(repr(vecteur_test)== "(3;-2;7)",msg=f"__repr__() donne: {vecteur_test.__repr__()}")
    
    def test_add(self):
        """Test d'addition de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) + Vecteur(-7,2,10) == Vecteur(-5,9,6), msg=f"__add__() donne: {Vecteur(2,7,-4) + Vecteur(-7,2,10)}")

    def test_add_null(self):
        """Test d'addition d'un vecteur null avec un vecteur ayant des valeurs"""
        self.assertTrue(Vecteur() + Vecteur(2,5,8.5) == Vecteur(2,5,8.5),  msg=f"__add__() donne: {Vecteur() + Vecteur(2,5,8.5)}")
    
    def test_add_err(self):
        """Test d'addition d'un nombre réel à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_reel = 8
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            vecteur_base + scalair_reel 

    def test_sub(self):
        """ Test soustraction de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) - Vecteur(-7,2,10) == Vecteur(9,5,-14), msg=f"__sub__() donne: {Vecteur(2,7,-4) - Vecteur(-7,2,10)}")

    def test_sub_null(self):
        """ Soustraction par un vecteur null"""
        self.assertTrue(Vecteur(2,5,8.5) - Vecteur() == Vecteur(2,5,8.5),  msg=f"__sub__() donne: {Vecteur(2,5,8.5)-Vecteur()}")
    
    def test_sub_err(self):
        """ Test de soustraction d'un nombre réel à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_reel = 8
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            vecteur_base - scalair_reel

    def test_mul_err(self):
        """ Test multiplication de deux vecteurs"""
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            Vecteur(2,7,-4) * Vecteur(-7,2,10)

    def test_mul_null(self):
        """ Test de multiplication par zéro"""
        self.assertTrue(Vecteur(2,5,8.5) * 0 == Vecteur(),  msg=f"__mul__() donne: {Vecteur(2,5,8.5)*0}")
    
    def test_mul(self):
        """ Test de multiplication d'un nombre réel à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_reel = 8
        self.assertTrue(vecteur_base * scalair_reel == Vecteur(40,-16,104), msg=f"__mul__() donne: {vecteur_base * scalair_reel}")

    def test_truediv_err(self):
        """ Test division de deux vecteurs"""
        with self.assertRaises(TypeError, msg = f"Aucune erreur n'a été trouvé"):
            Vecteur(2,7,-4) / Vecteur(-7,2,10)

    def test_truediv_err_0(self):
        """ Test division par zéro"""
        with self.assertRaises(ZeroDivisionError, msg = f"Aucune erreur n'a été trouvé"):
            Vecteur(2,7,-4) / 0

    def test_truediv_null(self):
        """ Test de vecteur null"""
        self.assertTrue(Vecteur() / 9 == Vecteur(),  msg=f"__truediv__() donne: {Vecteur()/9}")
    
    def test_truediv(self):
        """ Test de division d'un nombre réel à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_reel = 8
        self.assertTrue(vecteur_base / scalair_reel == Vecteur(5/8,-1/4,13/8), msg=f"__truediv__() donne: {vecteur_base / scalair_reel}")