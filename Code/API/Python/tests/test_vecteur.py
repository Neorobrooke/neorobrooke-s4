from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur

class TestVecteur(unittest.TestCase):
    """Test sur la classe Vecteur"""

    def test_repr(self):
        """Test d'un vecteur pour voir s'il se représente bien"""
        vecteur_test = Vecteur(3,-2,7)
        self.assertTrue(repr(vecteur_test)== "(3;-2;7)",msg=f"__repr__() donne: {vecteur_test.__repr__()}")
    
    def test_add(self):
        """Test d'addition de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) + Vecteur(-7,2,10) == Vecteur(-5,9,6), msg=f"Vecteur(2,7,-4) + Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) + Vecteur(-7,2,10)}")

    def test_add_nul(self):
        """Test d'addition d'un vecteur nul avec un vecteur ayant des valeurs"""
        self.assertTrue(Vecteur() + Vecteur(2,5,8.5) == Vecteur(2,5,8.5),  msg=f"Vecteur() + Vecteur(2,5,8.5) donne: {Vecteur() + Vecteur(2,5,8.5)}")
    
    def test_add_entier(self):
        """Test d'addition d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_entier = 8
        with self.assertRaises(TypeError, msg = f"L'addition avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            vecteur_base + scalair_entier 

    def test_sub(self):
        """Test soustraction de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) - Vecteur(-7,2,10) == Vecteur(9,5,-14), msg=f"Vecteur(2,7,-4) - Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) - Vecteur(-7,2,10)}")

    def test_sub_nul(self):
        """Soustraction par un vecteur nul"""
        self.assertTrue(Vecteur(2,5,8.5) - Vecteur() == Vecteur(2,5,8.5),  msg=f"Vecteur(2,5,8.5)-Vecteur() donne: {Vecteur(2,5,8.5)-Vecteur()}")
    
    def test_sub_entier(self):
        """Test de soustraction d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_entier = 8
        with self.assertRaises(TypeError, msg = f"La soustraction avec autre chose qu'un vecteur (comme un nombre réel) n'a pas levé d'exception de type TypeError"):
            vecteur_base - scalair_entier

    def test_mul_vecteur(self):
        """Test multiplication de deux vecteurs"""
        with self.assertRaises(TypeError, msg = f"La multiplication de deux vecteurs n'a pas levé d'exception de type TypeError"):
            Vecteur(2,7,-4) * Vecteur(-7,2,10)

    def test_mul_zero(self):
        """Test de multiplication par zéro"""
        self.assertTrue(Vecteur(2,5,8.5) * 0 == Vecteur(),  msg=f"Vecteur(2,5,8.5)*0 donne: {Vecteur(2,5,8.5)*0}")
    
    def test_mul_entier(self):
        """Test de multiplication d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_entier = 8
        self.assertTrue(vecteur_base * scalair_entier == Vecteur(40,-16,104), msg=f"Vecteur(5,-2,13) * 8 donne: {vecteur_base * scalair_entier}")

    def test_mul_reel(self):
        """Test de multiplication d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_reel = 8.45
        self.assertTrue(vecteur_base * scalair_reel == Vecteur(42.25,-16.9,109.85), msg=f"Vecteur(5,-2,13) * 8.45 donne: {vecteur_base * scalair_reel}")

    def test_truediv_vecteur(self):
        """Test division de deux vecteurs"""
        with self.assertRaises(TypeError, msg = f"La division d'un vecteur par un autre vecteur n'a pas levé d'exception de type TypeError"):
            Vecteur(2,7,-4) / Vecteur(-7,2,10)

    def test_truediv_division_par_zero(self):
        """Test division par zéro"""
        with self.assertRaises(ZeroDivisionError, msg = f"La division d'un vecteur par zéro n'a pas levé d'exception de type ZeroDivisionError"):
            Vecteur(2,7,-4) / 0

    def test_truediv_nul_par_entier(self):
        """Test divsion du vecteur nul par un entier"""
        self.assertTrue(Vecteur() / 9 == Vecteur(),  msg=f"Vecteur() / 9 donne: {Vecteur()/9}")
    
    def test_truediv_entier(self):
        """Test de division d'un vecteur par un nombre entier"""
        vecteur_base = Vecteur(5,-2,13)
        scalair_entier = 8
        self.assertTrue(vecteur_base / scalair_entier == Vecteur(5/8,-1/4,13/8), msg=f"Vecteur(5,-2,13) / 8 donne: {vecteur_base / scalair_entier}")
        