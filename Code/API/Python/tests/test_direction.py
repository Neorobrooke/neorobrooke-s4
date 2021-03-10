from __future__ import annotations
import unittest
from funibot_api.funibot import Direction

class TestsDirection(unittest.TestCase):

    def test_repr_Cas1(self):
        """ Cas fonctionnel, impose une valeur logique chaque variable"""
        directionCas1 = Direction("4x-8y+z")
        self.assertTrue(repr(directionCas1) == "Direction(x:4.0; y:-8.0; z:1.0)", msg=f"__repr__() donne: {repr(directionCas1)}")
    
    def test_repr_Cas2(self):
        """ Cas non fonctionnel, possede une valeur qui a un +-"""
        
        with self.assertRaises(ValueError, msg="Aucune erreur pour un double signe"):
            Direction("4x+-8y+z")
    
    """def test_repr_Cas3(self):
        " Cas non fonctionnel, possede pas de x"
        directionCas3 = Direction("4+8y+z")
        self.assertTrue(repr(directionCas3) == "Direction(x:4.0; y:-8.0; z:1.0)", msg=f"__repr__() donne: {repr(directionCas3)}")
    
     def test_repr_Cas4(self):
        " Cas non fonctionnel, possede une valeur qui a un +-"
        directionCas4 = Direction("4-8+2")
        self.assertTrue(repr(directionCas4) == "Direction(x:4.0; y:-8.0; z:1.0)", msg=f"__repr__() donne: {repr(directionCas4)}")
    """


