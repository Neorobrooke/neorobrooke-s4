import unittest
from funibot_api.funibot import PosVec, Poteau

class TestsPoteau(unittest.TestCase):

    def test_repr(self):
        position = PosVec(1,2,4)
        nom = "poteau_test"
        poteau = Poteau(nom="poteau_test", position=position)
        self.assertTrue(poteau.__repr__() == "Poteau[poteau_test](1;2;4)", msg=f"__repr__() donne: {poteau.__repr__()}")

    def truc(self):
        self.assertTrue(True)