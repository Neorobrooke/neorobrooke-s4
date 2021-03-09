from __future__ import annotations
from funibot_api.funibot_json_serial import FuniSerial
from typing import Union
from threading import Thread, ThreadError

from funibot_api.funibot_json_serial import MockSerial, MockType, IMockSerial


class DualMockSerial(IMockSerial):
    """Représente un mock série à deux canaux différents pour la lecture et l'écriture"""

    def __init__(self, canal_lecture: MockSerial = MockSerial(MockType.TEST), canal_ecriture: MockSerial = MockSerial(MockType.TEST)) -> None:
        self.lecture = canal_lecture
        self.ecriture = canal_ecriture

    def write(self, contenu: bytes) -> None:
        return self.ecriture.write(contenu=contenu)

    def readline(self) -> bytes:
        return self.lecture.readline()

    def read_all(self) -> bytes:
        return self.lecture.read_all()


class MockOpenCR(Thread):
    """Mock le OpenCR pour les tests"""

    def __init__(self, mock: DualMockSerial) -> None:

        self.serial: FuniSerial = FuniSerial(mock)
        pass

    def run(self):
        pass

    def shutdown(self):
        pass
