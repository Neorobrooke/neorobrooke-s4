from __future__ import annotations
import unittest
from funibot_api.funibot import Direction

class TestsDirection(unittest.TestCase):

    def test_repr_Normal(self):
        """ Impose une valeur logique chaque variable """
        directionCas1 = Direction("4x-8y+z")
        self.assertTrue(repr(directionCas1) == "Direction(x:4.0; y:-8.0; z:1.0)", msg=f"__repr__() donne: {repr(directionCas1)}")
    
    def test_repr_DoubleSigne(self):
        """ Double signe """
        with self.assertRaises(ValueError, msg="Aucune erreur pour un double signe"):
            Direction("4x+-8y+z")
    
    def test_repr_Variables(self):
        """ Autres caracteres que xyz """
        with self.assertRaises(ValueError, msg="Aucune erreur pour un autre caractères que xyz"):
            Direction("4x-8y+c")
    
    def test_repr_SansDirection(self):
        """ Sans caracteres que x ou y ou z """
        with self.assertRaises(ValueError, msg="Aucune erreur pour valeur sans direction"):
            Direction("4+4y+4z")
    
# deux fois la meme variables genre 4x+4x+y
# 

