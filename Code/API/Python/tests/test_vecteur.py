from __future__ import annotations
import unittest
from funibot_api.funibot import Vecteur

class TestVecteur(unittest.TestCase):
    """Test sur la classe Vecteur"""

    def test_repr(self):
        """Test d'un vecteur pour voir s'il se représente bien"""
        vecteur_test = Vecteur(3,-2,7)
        self.assertTrue(repr(vecteur_test) == "(3;-2;7)",msg = f"__repr__() donne: {vecteur_test.__repr__()}")
    
    def test_add(self):
        """Test d'addition de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) + Vecteur(-7,2,10) == Vecteur(-5,9,6), msg=f"Vecteur(2,7,-4) + Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) + Vecteur(-7,2,10)}")

    def test_add_nul(self):
        """Test d'addition d'un vecteur nul avec un vecteur ayant des valeurs"""
        self.assertTrue(Vecteur() + Vecteur(2,5,8.5) == Vecteur(2,5,8.5),  msg = f"Vecteur() + Vecteur(2,5,8.5) donne: {Vecteur() + Vecteur(2,5,8.5)}")
    
    def test_add_entier(self):
        """Test d'addition d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier = 8
        with self.assertRaises(TypeError, msg = f"L'addition avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            vecteur_base + scalaire_entier 

    def test_iadd(self):
        """Test d'addition += de deux vecteurs"""
        v = Vecteur(2,7,-4)
        v += Vecteur(-7,2,10)
        self.assertTrue(v == Vecteur(-5,9,6), msg = f"Vecteur(2,7,-4) += Vecteur(-7,2,10) donne: {v}")

    def test_iadd_nul(self):
        """Test d'addition += d'un vecteur nul avec un vecteur ayant des valeurs"""
        v = Vecteur()
        v += Vecteur(2,5,8.5)
        self.assertTrue(v == Vecteur(2,5,8.5),  msg = f"Vecteur() += Vecteur(2,5,8.5) donne: {v}")
    
    def test_iadd_entier(self):
        """Test d'addition += d'un nombre entier à un vecteur"""
        v = Vecteur(5,-2,13)
        with self.assertRaises(TypeError, msg = f"L'addition += avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            v += 8 

    def test_sub(self):
        """Test soustraction de deux vecteurs"""
        self.assertTrue(Vecteur(2,7,-4) - Vecteur(-7,2,10) == Vecteur(9,5,-14), msg = f"Vecteur(2,7,-4) - Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) - Vecteur(-7,2,10)}")

    def test_sub_nul(self):
        """Soustraction par un vecteur nul"""
        self.assertTrue(Vecteur(2,5,8.5) - Vecteur() == Vecteur(2,5,8.5),  msg = f"Vecteur(2,5,8.5) - Vecteur() donne: {Vecteur(2,5,8.5) - Vecteur()}")
    
    def test_sub_entier(self):
        """Test de soustraction d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier = 8
        with self.assertRaises(TypeError, msg = f"La soustraction avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            vecteur_base - scalaire_entier

    def test_isub(self):
        """Test de soustraction -= de deux vecteurs"""
        v = Vecteur(2,7,-4)
        v -= Vecteur(-7,2,10)
        self.assertTrue(v == Vecteur(9,5,-14), msg = f"Vecteur(2,7,-4) -= Vecteur(-7,2,10) donne: {v}")

    def test_isub_nul(self):
        """Test de soustraction -= d'un vecteur nul avec un vecteur ayant des valeurs"""
        v = Vecteur()
        v -= Vecteur(2,5,8.5)
        self.assertTrue(v == Vecteur(-2,-5,-8.5),  msg = f"Vecteur() -= Vecteur(2,5,8.5) donne: {v}")
    
    def test_isub_entier(self):
        """Test de soustraction -= d'un nombre entier à un vecteur"""
        v = Vecteur(5,-2,13)
        with self.assertRaises(TypeError, msg = f"La soustraction -= avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            v -= 8 

    def test_mul_vecteur(self):
        """Test multiplication de deux vecteurs"""
        with self.assertRaises(TypeError, msg = f"La multiplication de deux vecteurs n'a pas levé d'exception de type TypeError"):
            Vecteur(2,7,-4) * Vecteur(-7,2,10)

    def test_mul_zero(self):
        """Test de multiplication par zéro"""
        self.assertTrue(Vecteur(2,5,8.5) * 0 == Vecteur(),  msg = f"Vecteur(2,5,8.5) * 0 donne: {Vecteur(2,5,8.5) * 0}")
    
    def test_mul_entier(self):
        """Test de multiplication d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier = 8
        self.assertTrue(vecteur_base * scalaire_entier == Vecteur(40,-16,104), msg = f"Vecteur(5,-2,13) * 8 donne: {vecteur_base * scalaire_entier}")

    def test_mul_reel(self):
        """Test de multiplication d'un nombre réel à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_reel = 8.45
        self.assertTrue(vecteur_base * scalaire_reel == Vecteur(42.25,-16.9,109.85), msg = f"Vecteur(5,-2,13) * 8.45 donne: {vecteur_base * scalaire_reel}")
    
    def test_mul_entier_negatif(self):
        """Test de multiplication d'un nombre entier négatif à un vecteur"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier_negatif = -8
        self.assertTrue(vecteur_base * scalaire_entier_negatif == Vecteur(-40,16,-104), msg = f"Vecteur(5,-2,13) * -8 donne: {vecteur_base * scalaire_entier_negatif}")

    def test_imul_vecteur(self):
        """Test multiplication *= de deux vecteurs"""
        v = Vecteur(2,7,-4)
        with self.assertRaises(TypeError, msg = f"La multiplication *= de deux vecteurs n'a pas levé d'exception de type TypeError"):
            v *= Vecteur(-7,2,10)

    def test_imul_zero(self):
        """Test de multiplication *= par zéro"""
        v = Vecteur(2,5,8.5)
        v *= 0
        self.assertTrue(v == Vecteur(),  msg = f"Vecteur(2,5,8.5) *= 0 donne: {v}")
    
    def test_imul_entier(self):
        """Test de multiplication *= d'un nombre entier à un vecteur"""
        v = Vecteur(5,-2,13)
        v *= 8
        self.assertTrue(v == Vecteur(40,-16,104), msg = f"Vecteur(5,-2,13) *= 8 donne: {v}")

    def test_imul_reel(self):
        """Test de multiplication *= d'un nombre réel à un vecteur"""
        v = Vecteur(5,-2,13)
        v *= 8.45
        self.assertTrue(v == Vecteur(42.25,-16.9,109.85), msg = f"Vecteur(5,-2,13) *= 8.45 donne: {v}")
    
    def test_imul_entier_negatif(self):
        """Test de multiplication d'un nombre entier négatif à un vecteur"""
        v = Vecteur(5,-2,13)
        v *= -8
        self.assertTrue(v == Vecteur(-40,16,-104), msg = f"Vecteur(5,-2,13) *= -8 donne: {v}")

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
        self.assertTrue(Vecteur() / 9 == Vecteur(),  msg = f"Vecteur() / 9 donne: {Vecteur() / 9}")
    
    def test_truediv_entier(self):
        """Test de division d'un vecteur par un nombre entier"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier = 8
        self.assertTrue(vecteur_base / scalaire_entier == Vecteur(5/8,-1/4,13/8), msg = f"Vecteur(5,-2,13) / 8 donne: {vecteur_base / scalaire_entier}")

    def test_truediv_reel(self):
        """Test de division d'un vecteur par un nombre réel"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_reel = 2.5
        self.assertTrue(vecteur_base / scalaire_reel == Vecteur(2,-0.8,5.2), msg = f"Vecteur(5,-2,13) / 2.5 donne: {vecteur_base / scalaire_reel}")

    def test_truediv_entier_negatif(self):
        """Test de division d'un vecteur par un nombre entier négatif"""
        vecteur_base = Vecteur(5,-2,13)
        scalaire_entier_negatif = -8
        self.assertTrue(vecteur_base / scalaire_entier_negatif == Vecteur(-5/8,1/4,-13/8), msg = f"Vecteur(5,-2,13) / -8 donne: {vecteur_base / scalaire_entier_negatif}")
