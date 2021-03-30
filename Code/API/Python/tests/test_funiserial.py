from __future__ import annotations

from funibot_api.funiserial import FuniErreur, FuniSerial, eFuniErreur
from tests.mock_serial import MockSerial, MockType, DualMockSerial
import unittest

class TestFuniErreur(unittest.TestCase):
    """Tests sur la classe FuniErreur"""
    
    def CreationTexte(self):
        pass

    def CreationEntier(self):
        pass

    def Representation(self):
        pass

class TestsFuniSerial(unittest.TestCase):
    """Test sur la classe FuniSerial"""

    def SetUp(self):
        """Initialisation commune à plusieurs tests"""
        self.mock = MockSerial(MockType.TEST)
        self.emock = MockSerial(MockType.TEST)
        self.dmock = DualMockSerial(canal_lecture=self.mock, canal_ecriture=self.emock)

    #def test_init(self):
     #   """Test d'initialisation d'un FuniSerial"""
      #  bot = FuniSerial(self.mock)
