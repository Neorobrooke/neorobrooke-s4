from __future__ import annotations
import unittest
from funibot_api.funilib import Vecteur, ChangerNormeVecteurNulErreur


class TestVecteur(unittest.TestCase):
    """Test sur la classe Vecteur"""

    def test_repr(self):
        """Test d'un vecteur pour voir s'il se représente bien"""
        vecteur_test = Vecteur(3, -2, 7)
        self.assertTrue(repr(vecteur_test) == "(3;-2;7)",
                        msg=f"__repr__() donne: {vecteur_test.__repr__()}")

    def test_add(self):
        """Test d'addition de deux vecteurs"""
        self.assertTrue(Vecteur(2, 7, -4) + Vecteur(-7, 2, 10) == Vecteur(-5, 9, 6),
                        msg=f"Vecteur(2,7,-4) + Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) + Vecteur(-7,2,10)}")

    def test_add_nul(self):
        """Test d'addition d'un vecteur nul avec un vecteur ayant des valeurs"""
        self.assertTrue(Vecteur() + Vecteur(2, 5, 8.5) == Vecteur(2, 5, 8.5),
                        msg=f"Vecteur() + Vecteur(2,5,8.5) donne: {Vecteur() + Vecteur(2,5,8.5)}")

    def test_add_entier(self):
        """Test d'addition d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        with self.assertRaises(TypeError, msg=f"L'addition avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            vecteur_base + scalaire_entier

    def test_add_none(self):
        """Test d'addition de deux vecteurs avec un None dans un des vecteurs"""
        vecteur_base = Vecteur(5, -2, 13)
        vecteur_none = Vecteur(1, 5, None)
        with self.assertRaises(TypeError, msg=f"L'addition de deux vecteurs avec un vecteur ayant un None n'a pas levé d'exception de type TypeError"):
            vecteur_base + vecteur_none

    def test_iadd(self):
        """Test d'addition += de deux vecteurs"""
        v = Vecteur(2, 7, -4)
        v += Vecteur(-7, 2, 10)
        self.assertTrue(v == Vecteur(-5, 9, 6),
                        msg=f"Vecteur(2,7,-4) += Vecteur(-7,2,10) donne: {v}")

    def test_iadd_nul(self):
        """Test d'addition += d'un vecteur nul avec un vecteur ayant des valeurs"""
        v = Vecteur()
        v += Vecteur(2, 5, 8.5)
        self.assertTrue(v == Vecteur(2, 5, 8.5),
                        msg=f"Vecteur() += Vecteur(2,5,8.5) donne: {v}")

    def test_iadd_entier(self):
        """Test d'addition += d'un nombre entier à un vecteur"""
        v = Vecteur(5, -2, 13)
        with self.assertRaises(TypeError, msg=f"L'addition += avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            v += 8

    def test_iadd_none(self):
        """Test d'addition += de deux vecteurs avec un None dans un des vecteurs"""
        vecteur_base = Vecteur(5, -2, 13)
        with self.assertRaises(TypeError, msg=f"L'addition += de deux vecteurs avec un vecteur ayant un None n'a pas levé d'exception de type TypeError"):
            vecteur_base += Vecteur(1, 5, None)
        self.assertTrue(Vecteur(5, -2, 13) == vecteur_base,
                        msg=f"Après l'erreur d'addition +=, le vecteur {Vecteur(5,-2,13)} n'égale pas {vecteur_base}")

    def test_sub(self):
        """Test soustraction de deux vecteurs"""
        self.assertTrue(Vecteur(2, 7, -4) - Vecteur(-7, 2, 10) == Vecteur(9, 5, -14),
                        msg=f"Vecteur(2,7,-4) - Vecteur(-7,2,10) donne: {Vecteur(2,7,-4) - Vecteur(-7,2,10)}")

    def test_sub_nul(self):
        """Soustraction par un vecteur nul"""
        self.assertTrue(Vecteur(2, 5, 8.5) - Vecteur() == Vecteur(2, 5, 8.5),
                        msg=f"Vecteur(2,5,8.5) - Vecteur() donne: {Vecteur(2,5,8.5) - Vecteur()}")

    def test_sub_entier(self):
        """Test de soustraction d'un nombre entier à un vecteur"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        with self.assertRaises(TypeError, msg=f"La soustraction avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            vecteur_base - scalaire_entier

    def test_sub_none(self):
        """Test de soustraction de deux vecteurs avec un None dans un des vecteurs"""
        vecteur_base = Vecteur(5, -2, 13)
        vecteur_none = Vecteur(1, 5, None)
        with self.assertRaises(TypeError, msg=f"La soustraction de deux vecteurs avec un vecteur ayant un None n'a pas levé d'exception de type TypeError"):
            vecteur_base - vecteur_none

    def test_isub(self):
        """Test de soustraction -= de deux vecteurs"""
        v = Vecteur(2, 7, -4)
        v -= Vecteur(-7, 2, 10)
        self.assertTrue(v == Vecteur(9, 5, -14),
                        msg=f"Vecteur(2,7,-4) -= Vecteur(-7,2,10) donne: {v}")

    def test_isub_nul(self):
        """Test de soustraction -= d'un vecteur nul avec un vecteur ayant des valeurs"""
        v = Vecteur()
        v -= Vecteur(2, 5, 8.5)
        self.assertTrue(v == Vecteur(-2, -5, -8.5),
                        msg=f"Vecteur() -= Vecteur(2,5,8.5) donne: {v}")

    def test_isub_entier(self):
        """Test de soustraction -= d'un nombre entier à un vecteur"""
        v = Vecteur(5, -2, 13)
        with self.assertRaises(TypeError, msg=f"La soustraction -= avec autre chose qu'un vecteur (comme un scalaire) n'a pas levé d'exception de type TypeError"):
            v -= 8

    def test_isub_none(self):
        """Test de soustraction -= de deux vecteurs avec un None dans un des vecteurs"""
        vecteur_base = Vecteur(5, -2, 13)
        with self.assertRaises(TypeError, msg=f"La soustraction -= de deux vecteurs avec un vecteur ayant un None n'a pas levé d'exception de type TypeError"):
            vecteur_base -= Vecteur(1, 5, None)
        self.assertTrue(Vecteur(5, -2, 13) == vecteur_base,
                        msg=f"Après l'erreur de soustraction -=, le vecteur {Vecteur(5,-2,13)} n'égale pas {vecteur_base}")

    def test_mul_vecteur(self):
        """Test multiplication de deux vecteurs (vecteur * scalaire)"""
        with self.assertRaises(TypeError, msg=f"La multiplication de deux vecteurs n'a pas levé d'exception de type TypeError"):
            Vecteur(2, 7, -4) * Vecteur(-7, 2, 10)

    def test_mul_zero(self):
        """Test de multiplication par zéro (vecteur * scalaire)"""
        self.assertTrue(Vecteur(2, 5, 8.5) * 0 == Vecteur(),
                        msg=f"Vecteur(2,5,8.5) * 0 donne: {Vecteur(2,5,8.5) * 0}")

    def test_mul_entier(self):
        """Test de multiplication d'un nombre entier à un vecteur (vecteur * scalaire)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        self.assertTrue(vecteur_base * scalaire_entier == Vecteur(40, -16, 104),
                        msg=f"Vecteur(5,-2,13) * 8 donne: {vecteur_base * scalaire_entier}")

    def test_mul_reel(self):
        """Test de multiplication d'un nombre réel à un vecteur (vecteur * scalaire)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_reel = 8.45
        self.assertTrue(vecteur_base * scalaire_reel == Vecteur(42.25, -16.9, 109.85),
                        msg=f"Vecteur(5,-2,13) * 8.45 donne: {vecteur_base * scalaire_reel}")

    def test_mul_entier_negatif(self):
        """Test de multiplication d'un nombre entier négatif à un vecteur (vecteur * scalaire)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier_negatif = -8
        self.assertTrue(vecteur_base * scalaire_entier_negatif == Vecteur(-40, 16, -104),
                        msg=f"Vecteur(5,-2,13) * -8 donne: {vecteur_base * scalaire_entier_negatif}")

    def test_mul_none(self):
        """Test de multiplication d'un vecteur ayant un None et un scalaire (vecteur * scalaire)"""
        vecteur_none = Vecteur(5, -2, None)
        scalaire = 4
        with self.assertRaises(TypeError, msg=f"La multiplicaiton d'un vecteur ayant un None et un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none * scalaire

    def test_rmul_zero(self):
        """Test de multiplication par zéro (sclaire * vecteur)"""
        self.assertTrue(0 * Vecteur(2, 5, 8.5) == Vecteur(),
                        msg=f"0 * Vecteur(2,5,8.5) donne: {0 * Vecteur(2,5,8.5)}")

    def test_rmul_entier(self):
        """Test de multiplication d'un nombre entier à un vecteur (sclaire * vecteur)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        self.assertTrue(scalaire_entier * vecteur_base == Vecteur(40, -16, 104),
                        msg=f"8 * Vecteur(5,-2,13) donne: {scalaire_entier * vecteur_base}")

    def test_rmul_reel(self):
        """Test de multiplication d'un nombre réel à un vecteur (sclaire * vecteur)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_reel = 8.45
        self.assertTrue(scalaire_reel * vecteur_base == Vecteur(42.25, -16.9, 109.85),
                        msg=f"8.45 * Vecteur(5,-2,13) donne: {scalaire_reel * vecteur_base}")

    def test_rmul_entier_negatif(self):
        """Test de multiplication d'un nombre entier négatif à un vecteur (sclaire * vecteur)"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier_negatif = -8
        self.assertTrue(scalaire_entier_negatif * vecteur_base == Vecteur(-40, 16, -104),
                        msg=f"-8 * Vecteur(5,-2,13) donne: {scalaire_entier_negatif * vecteur_base}")

    def test_rmul_none(self):
        """Test de multiplication d'un vecteur ayant un None et un scalaire (sclaire * vecteur)"""
        vecteur_none = Vecteur(5, -2, None)
        scalaire = 4
        with self.assertRaises(TypeError, msg=f"La multiplicaiton d'un scalaire avec un vecteur ayant un None n'a pas levé d'exception de type TypeError"):
            scalaire * vecteur_none

    def test_imul_vecteur(self):
        """Test multiplication *= de deux vecteurs"""
        v = Vecteur(2, 7, -4)
        with self.assertRaises(TypeError, msg=f"La multiplication *= de deux vecteurs n'a pas levé d'exception de type TypeError"):
            v *= Vecteur(-7, 2, 10)

    def test_imul_zero(self):
        """Test de multiplication *= par zéro"""
        v = Vecteur(2, 5, 8.5)
        v *= 0
        self.assertTrue(
            v == Vecteur(),  msg=f"Vecteur(2,5,8.5) *= 0 donne: {v}")

    def test_imul_entier(self):
        """Test de multiplication *= d'un nombre entier à un vecteur"""
        v = Vecteur(5, -2, 13)
        v *= 8
        self.assertTrue(v == Vecteur(40, -16, 104),
                        msg=f"Vecteur(5,-2,13) *= 8 donne: {v}")

    def test_imul_reel(self):
        """Test de multiplication *= d'un nombre réel à un vecteur"""
        v = Vecteur(5, -2, 13)
        v *= 8.45
        self.assertTrue(v == Vecteur(42.25, -16.9, 109.85),
                        msg=f"Vecteur(5,-2,13) *= 8.45 donne: {v}")

    def test_imul_entier_negatif(self):
        """Test de multiplication d'un nombre entier négatif à un vecteur"""
        v = Vecteur(5, -2, 13)
        v *= -8
        self.assertTrue(v == Vecteur(-40, 16, -104),
                        msg=f"Vecteur(5,-2,13) *= -8 donne: {v}")

    def test_imul_none(self):
        """Test de multiplication *= d'un vecteur ayant un None et d'un scalaire"""
        vecteur_none = Vecteur(5, -2, None)
        with self.assertRaises(TypeError, msg=f"La multiplicaiton *= d'un vecteur ayant un None et d'un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none *= 4
        self.assertTrue(Vecteur(5, -2, None) == vecteur_none,
                        msg=f"Après l'erreur de multiplicaiton *=, le vecteur {Vecteur(5,-2,None)} n'égale pas {vecteur_none}")

    def test_truediv_vecteur(self):
        """Test division de deux vecteurs"""
        with self.assertRaises(TypeError, msg=f"La division d'un vecteur par un autre vecteur n'a pas levé d'exception de type TypeError"):
            Vecteur(2, 7, -4) / Vecteur(-7, 2, 10)

    def test_truediv_division_par_zero(self):
        """Test division par zéro"""
        with self.assertRaises(ZeroDivisionError, msg=f"La division d'un vecteur par zéro n'a pas levé d'exception de type ZeroDivisionError"):
            Vecteur(2, 7, -4) / 0

    def test_truediv_nul_par_entier(self):
        """Test divsion du vecteur nul par un entier"""
        self.assertTrue(Vecteur() / 9 == Vecteur(),
                        msg=f"Vecteur() / 9 donne: {Vecteur() / 9}")

    def test_truediv_entier(self):
        """Test de division d'un vecteur par un nombre entier"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        self.assertTrue(vecteur_base / scalaire_entier == Vecteur(5/8, -1/4, 13/8),
                        msg=f"Vecteur(5,-2,13) / 8 donne: {vecteur_base / scalaire_entier}")

    def test_truediv_reel(self):
        """Test de division d'un vecteur par un nombre réel"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_reel = 2.5
        self.assertTrue(vecteur_base / scalaire_reel == Vecteur(2, -0.8, 5.2),
                        msg=f"Vecteur(5,-2,13) / 2.5 donne: {vecteur_base / scalaire_reel}")

    def test_truediv_entier_negatif(self):
        """Test de division d'un vecteur par un nombre entier négatif"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier_negatif = -8
        self.assertTrue(vecteur_base / scalaire_entier_negatif == Vecteur(-5/8, 1/4, -13/8),
                        msg=f"Vecteur(5,-2,13) / -8 donne: {vecteur_base / scalaire_entier_negatif}")

    def test_truediv_none(self):
        """Test de division d'un vecteur ayant un None avec un scalaire"""
        vecteur_none = Vecteur(5, -2, None)
        scalaire = 4
        with self.assertRaises(TypeError, msg=f"La division d'un vecteur ayant un None par un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none / scalaire

    def test_itruediv_vecteur(self):
        """Test division /= de deux vecteurs"""
        v = Vecteur(2, 7, -4)
        with self.assertRaises(TypeError, msg=f"La division /= d'un vecteur par un autre vecteur n'a pas levé d'exception de type TypeError"):
            v /= Vecteur(-7, 2, 10)

    def test_itruediv_division_par_zero(self):
        """Test division /= par zéro"""
        v = Vecteur(2, 7, -4)
        with self.assertRaises(ZeroDivisionError, msg=f"La division /= d'un vecteur par zéro n'a pas levé d'exception de type ZeroDivisionError"):
            v /= 0

    def test_itruediv_nul_par_entier(self):
        """Test divsion /= du vecteur nul par un entier"""
        v = Vecteur()
        v /= 9
        self.assertTrue(v == Vecteur(),  msg=f"Vecteur() /= 9 donne: {v}")

    def test_itruediv_entier(self):
        """Test de division /= d'un vecteur par un nombre entier"""
        v = Vecteur(5, -2, 13)
        v /= 8
        self.assertTrue(v == Vecteur(5/8, -1/4, 13/8),
                        msg=f"Vecteur(5,-2,13) /= 8 donne: {v}")

    def test_itruediv_reel(self):
        """Test de division /= d'un vecteur par un nombre réel"""
        v = Vecteur(5, -2, 13)
        v /= 2.5
        self.assertTrue(v == Vecteur(2, -0.8, 5.2),
                        msg=f"Vecteur(5,-2,13) /= 2.5 donne: {v}")

    def test_itruediv_entier_negatif(self):
        """Test de division /= d'un vecteur par un nombre entier négatif"""
        v = Vecteur(5, -2, 13)
        v /= -8
        self.assertTrue(v == Vecteur(-5/8, 1/4, -13/8),
                        msg=f"Vecteur(5,-2,13) /= -8 donne: {v}")

    def test_itruediv_none(self):
        """Test de division /= d'un vecteur ayant un None par un scalaire"""
        vecteur_none = Vecteur(5, -2, None)
        with self.assertRaises(TypeError, msg=f"La division /= d'un vecteur ayant un None par un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none /= 4
        self.assertTrue(Vecteur(5, -2, None) == vecteur_none,
                        msg=f"Après l'erreur de division /=, le vecteur {Vecteur(5,-2,None)} n'égale pas {vecteur_none}")

    def test_floordiv_vecteur(self):
        """Test division // de deux vecteurs"""
        with self.assertRaises(TypeError, msg=f"La division // d'un vecteur par un autre vecteur n'a pas levé d'exception de type TypeError"):
            Vecteur(2.3, 7, -4) // Vecteur(-7, 2.1, 10)

    def test_floordiv_division_par_zero(self):
        """Test division // par zéro"""
        with self.assertRaises(ZeroDivisionError, msg=f"La division // d'un vecteur par zéro n'a pas levé d'exception de type ZeroDivisionError"):
            Vecteur(2, 7, -4) // 0

    def test_floordiv_nul_par_entier(self):
        """Test divsion // du vecteur nul par un entier"""
        self.assertTrue(Vecteur() // 9 == Vecteur(),
                        msg=f"Vecteur() // 9 donne: {Vecteur() // 9}")

    def test_floordiv_entier(self):
        """Test de division // d'un vecteur par un nombre entier"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_entier = 8
        self.assertTrue(vecteur_base // scalaire_entier == Vecteur(0, -1, 1),
                        msg=f"Vecteur(5,-2,13) // 8 donne: {vecteur_base // scalaire_entier}")

    def test_floordiv_reel(self):
        """Test de division // d'un vecteur par un nombre réel"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_reel = 2.5
        self.assertTrue(vecteur_base // scalaire_reel == Vecteur(2.0, -1.0, 5.0),
                        msg=f"Vecteur(5,-2,13) // 2.5 donne: {vecteur_base // scalaire_reel}")

    def test_floordiv_reel_negatif(self):
        """Test de division // d'un vecteur par un nombre réel négatif"""
        vecteur_base = Vecteur(5, -2, 13)
        scalaire_reel_negatif = -1.5
        self.assertTrue(vecteur_base // scalaire_reel_negatif == Vecteur(-4.0, 1.0, -9.0),
                        msg=f"Vecteur(5,-2,13) // -1.5 donne: {vecteur_base // scalaire_reel_negatif}")

    def test_floordiv_none(self):
        """Test de division // d'un vecteur ayant un None par un scalaire"""
        vecteur_none = Vecteur(5, -2, None)
        scalaire = 4
        with self.assertRaises(TypeError, msg=f"La division // d'un vecteur ayant un None par un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none // scalaire

    def test_ifloordiv_vecteur(self):
        """Test division //= de deux vecteurs"""
        v = Vecteur(2.3, 7, -4)
        with self.assertRaises(TypeError, msg=f"La division //= d'un vecteur par un autre vecteur n'a pas levé d'exception de type TypeError"):
            v //= Vecteur(-7, 2.1, 10)

    def test_ifloordiv_division_par_zero(self):
        """Test division //= par zéro"""
        v = Vecteur(2, 7, -4)
        with self.assertRaises(ZeroDivisionError, msg=f"La division //= d'un vecteur par zéro n'a pas levé d'exception de type ZeroDivisionError"):
            v // 0

    def test_ifloordiv_nul_par_entier(self):
        """Test divsion //= du vecteur nul par un entier"""
        v = Vecteur()
        v //= 9
        self.assertTrue(v == Vecteur(),  msg=f"Vecteur() //= 9 donne: {v}")

    def test_ifloordiv_entier(self):
        """Test de division //= d'un vecteur par un nombre entier"""
        v = Vecteur(5, -2, 13)
        v //= 8
        self.assertTrue(v == Vecteur(0, -1, 1),
                        msg=f"Vecteur(5,-2,13) //= 8 donne: {v}")

    def test_ifloordiv_reel(self):
        """Test de division //= d'un vecteur par un nombre réel"""
        v = Vecteur(5, -2, 13)
        v //= 2.5
        self.assertTrue(v == Vecteur(2.0, -1.0, 5.0),
                        msg=f"Vecteur(5,-2,13) //= 2.5 donne: {v}")

    def test_ifloordiv_reel_negatif(self):
        """Test de division //= d'un vecteur par un nombre réel négatif"""
        v = Vecteur(5, -2, 13)
        v //= -1.5
        self.assertTrue(v == Vecteur(-4.0, 1.0, -9.0),
                        msg=f"Vecteur(5,-2,13) //= -1.5 donne: {v}")

    def test_ifloordiv_none(self):
        """Test de division //= d'un vecteur ayant un None par un scalaire"""
        vecteur_none = Vecteur(5, -2, None)
        with self.assertRaises(TypeError, msg=f"La division /= d'un vecteur ayant un None par un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_none //= 4
        self.assertTrue(Vecteur(5, -2, None) == vecteur_none,
                        msg=f"Après l'erreur de division //=, le vecteur {Vecteur(5,-2,None)} n'égale pas {vecteur_none}")

    def test_unitaire(self):
        """Test vecteur unitaire"""
        self.assertTrue(Vecteur(2, -5, 3).unitaire() == Vecteur(0.3244428422615251, -0.8111071056538127,
                        0.48666426339228763), msg=f"Le vecteur unitaire de Vecteur(2,-5,3) donne: {Vecteur(2,-5,3).unitaire()}")

    def test_unitaire_vecteur_nul(self):
        """Test vecteur unitaire du vecteur nul"""
        self.assertTrue(Vecteur().unitaire() == Vecteur(
        ), msg=f"Le vecteur unitaire du vecteur nul donne: {Vecteur().unitaire()}")

    def test_ne(self):
        """Test vecteur non égaux"""
        self.assertTrue(Vecteur(1, 2, 3) != Vecteur(
            1, 2, 4), msg=f"Les vecteurs {Vecteur(1,2,3)} et {Vecteur(1,2,4)} sont égaux")

    def test_norme(self):
        """Test de la norme d'un vecteur"""
        self.assertTrue(Vecteur(3, 4, 0).norme == 5,
                        msg=f"La norme du Vecteur(3,4,0) donne: {Vecteur(3,4,0).norme}")

    def test_norme_null(self):
        """Test de la norme du vecteur null"""
        self.assertTrue(Vecteur(0, 0, 0).norme == 0,
                        msg=f"La norme du Vecteur(0,0,0) donne: {Vecteur(0,0,0).norme}")

    def test_norme_none(self):
        """Test de la norme d'un vecteur ayant un None"""
        with self.assertRaises(TypeError, msg=f"La norme d'un vecteur ayant None n'a pas levé d'exception de type TypeError"):
            Vecteur(3, 4, None).norme == 5

    def test_norme_changement(self):
        """Test du changement de norme"""
        vecteur_base = Vecteur(3, 4, 0)
        vecteur_base.norme = 2.5
        self.assertTrue(vecteur_base.x == 1.5,
                        msg=f"La composante en x du Vecteur(3,4,0) en imposant sa norme à 2.5 donne: {vecteur_base.x}")
        self.assertTrue(
            vecteur_base.y == 2, msg=f"La composante en y du Vecteur(3,4,0) en imposant sa norme à 2.5 donne: {vecteur_base.y}")
        self.assertTrue(
            vecteur_base.z == 0, msg=f"La composante en z du Vecteur(3,4,0) en imposant sa norme à 2.5 donne: {vecteur_base.z}")

    def test_norme_changement_pour_0(self):
        """Test du changement de norme par 0"""
        vecteur_base = Vecteur(3, 4, 0)
        vecteur_base.norme = 0
        self.assertTrue(
            vecteur_base.x == 0, msg=f"La composante en x du Vecteur(3,4,0) en imposant sa norme à 0 donne: {vecteur_base.x}")
        self.assertTrue(
            vecteur_base.y == 0, msg=f"La composante en y du Vecteur(3,4,0) en imposant sa norme à 0 donne: {vecteur_base.y}")
        self.assertTrue(
            vecteur_base.z == 0, msg=f"La composante en z du Vecteur(3,4,0) en imposant sa norme à 0 donne: {vecteur_base.z}")

    def test_norme_changement_vecteur_null(self):
        """Test du changement de norme d'un vecteur null"""
        vecteur_null = Vecteur(0, 0, 0)
        with self.assertRaises(ChangerNormeVecteurNulErreur, msg=f"La modification de la norme d'un vecteur null n'a pas levé d'exception de type ChangerNormeVecteurNulErreur"):
            vecteur_null.norme = 2.5

    def test_norme_changement_none(self):
        """Test du changement de norme par un None"""
        vecteur_base = Vecteur(3, 4, 0)
        with self.assertRaises(TypeError, msg=f"La division /= d'un vecteur ayant un None par un scalaire n'a pas levé d'exception de type TypeError"):
            vecteur_base.norme = None
        self.assertTrue(
            vecteur_base.x == 3, msg=f"Après l'erreur du changement de norme, la composante en x du vecteur modifié {vecteur_base.x} n'égale pas la composante en x du vecteur de base 3")
        self.assertTrue(
            vecteur_base.y == 4, msg=f"Après l'erreur du changement de norme, la composante en y du vecteur modifié {vecteur_base.y} n'égale pas la composante en y du vecteur de base 4")
        self.assertTrue(
            vecteur_base.z == 0, msg=f"Après l'erreur du changement de norme, la composante en z du vecteur modifié {vecteur_base.z} n'égale pas la composante en z du vecteur de base 0")

    def test_tuple(self):
        """Test de la création d'un tuple"""
        v = Vecteur(1, 2, 3)
        v_tuple = v.vers_tuple()
        self.assertTrue(type(v_tuple) == tuple,
                        msg=f"La création d'un tuple à partir du vecteur n'a pas fonctionné")
        self.assertTrue(
            v_tuple[0] == v.x, msg=f"La valeur du Tuple à la position 0, {v_tuple[0]} n'égale pas la composante en x du Vecteur de départ, {v.x}")
        self.assertTrue(
            v_tuple[1] == v.y, msg=f"La valeur du Tuple à la position 1, {v_tuple[1]} n'égale pas la composante en y du Vecteur de départ, {v.y}")
        self.assertTrue(
            v_tuple[2] == v.z, msg=f"La valeur du Tuple à la position 2, {v_tuple[2]} n'égale pas la composante en z du Vecteur de départ, {v.z}")
