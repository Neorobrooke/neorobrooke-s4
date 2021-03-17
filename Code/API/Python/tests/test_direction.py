from __future__ import annotations
import unittest
from funibot_api.funibot import Direction

class TestsDirection(unittest.TestCase):

    def test_repr_normal(self):
        """Test de la représentation d'une direction"""
        direction = Direction("4x-8y+z")
        self.assertTrue(repr(direction) == "Direction(x:4.0; y:-8.0; z:1.0)", msg = f"__repr__() donne: {repr(direction)}")
    
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

    
# deux fois la meme variables genre 4x+4x+y
# 

