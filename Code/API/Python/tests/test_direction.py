from __future__ import annotations
import unittest
from funibot_api.funilib import Direction, Vecteur

class TestsDirection(unittest.TestCase):

    def test_repr_normal(self):
        """Test de la représentation d'une direction"""
        direction = Direction("4x-8y+z")
        self.assertTrue(repr(direction) == "Direction(x:4; y:-8; z:1)", msg = f"__repr__() donne: {repr(direction)}")
    
    def test_repr_double_signe(self):
        """Test de la représentation d'une direction ayant deux signes"""
        with self.assertRaises(ValueError, msg = "La présence d'un double signe dans la direction n'a pas levé d'exception de type ValueError"):
            Direction("4x+-8y+z")
    
    def test_repr_variables(self):
        """Test de la direction avec d'autres caracteres que xyz"""
        with self.assertRaises(ValueError, msg = "La présence d'autres caracteres que xyz dans la direction n'a pas levé d'exception de type ValueError"):
            Direction("4x-8y+c")
    
    def test_repr_sans_direction(self):
        """Test de la représentation d'une direction en ne mettant pas un des caracteres"""
        with self.assertRaises(ValueError, msg = "L'absence d'un caractere dans la direction n'a pas levé d'exception de type ValueError") as re:
            Direction("4+4y+4z")
        self.assertEqual(str(re.exception), "Double signe ou signe ailleurs qu'au début")

    def test_repr_double_variable(self):
        """Test de la représentation d'une direction en mettant deux caractères identiques"""
        with self.assertRaises(ValueError, msg = "Avoir deux fois le même caractère n'a pas levé d'exception de type ValueError") as re:
            Direction("4x+4x+4y")
        self.assertEqual(str(re.exception), "L'axe <x> apparaît plusieurs fois")

    def test_repr_null(self):
        """Test de la représentation d'une direction null"""
        direction = Direction("0")
        self.assertTrue(repr(direction) == "Direction(x:0; y:0; z:0)", msg = f"La représentation d'une direction null donne: {repr(direction)}")

    def test_repr_un_entier(self):
        """Test de la représentation d'une direction avec un entier sans composante"""
        with self.assertRaises(ValueError, msg = "Avoir une direction contenant un entier sans composante n'a pas levé d'exception de type ValueError"):
            Direction("12")

    def test_repr_deux_composantes(self):
        """Test de la représentation d'une direction avec 2 composantes"""
        direction = Direction("2x+8z")
        self.assertTrue(repr(direction) == "Direction(x:2; y:0; z:8)", msg = f"La représentation d'une direction avec deux composantes donne: {repr(direction)}")

    def test_repr_distance_vecteur(self):
        """Test de la représentation d'une direction en vecteur"""
        direction = Direction("2x+8z")
        dir_vect = direction.vecteur()
        self.assertTrue(direction.axe_x == dir_vect.x, msg = f"La composante en x de la direction en vecteur donne: {dir_vect.x}")
        self.assertTrue(direction.axe_y == dir_vect.y, msg = f"La composante en y de la direction en vecteur donne: {dir_vect.y}")
        self.assertTrue(direction.axe_z == dir_vect.z, msg = f"La composante en z de la direction en vecteur donne: {dir_vect.z}")

    def test_repr_reel(self):
        """Test de la représentation d'une direction avec des nombres réels"""
        direction = Direction("2.6x+8.1z")
        self.assertTrue(repr(direction) == "Direction(x:2.6; y:0; z:8.1)", msg = f"La représentation d'une direction avec des réels donne: {repr(direction)}")

    def test_repr_deux_points_separer(self):
        """Test avec réel de type 3.4.5 de la représentation d'une direction"""
        with self.assertRaises(ValueError, msg = "Avoir une direction contenant un réel avec deux points de type 3.4.5 n'a pas levé d'exception de type ValueError"):
            Direction("2.6.5x+8.1z")

    def test_repr_fausse_reel(self):
        """Test avec réel de type 3..2 de la représentation d'une direction"""
        with self.assertRaises(ValueError, msg = "Avoir une direction contenant un réel avec deux points de type 3..2 n'a pas levé d'exception de type ValueError"):
            Direction("2.5x+8..1z")

    def test_repr_vigule_reel(self):
        """Test de la représentation d'une direction avec une virgule"""
        direction = Direction("2,6x+2y+8,1z")
        self.assertTrue(repr(direction) == "Direction(x:2.6; y:2; z:8.1)", msg = f"La représentation d'une direction avec des virgules donne: {repr(direction)}")
        
    #@unittest.skip("Pas prêt, test avec float")
# faire comparaison avec .axe_x == et non reps