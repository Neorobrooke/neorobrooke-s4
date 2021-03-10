import unittest
from funibot_api.funibot import Direction

class TestsDirection(unittest.TestCase):

    def test_repr_Cas1(self):
        """ Cas fonctionnel, impose une valeur logique chaque variable"""
        direction = Direction("4x-8y+z")
        self.assertTrue(direction.__repr__() == "Direction(x:4.0; y:-8.0; z:1.0)", msg=f"__repr__() donne: {direction.__repr__()}")