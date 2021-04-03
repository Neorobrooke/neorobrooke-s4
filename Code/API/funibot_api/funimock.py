from __future__ import annotations

from enum import Enum, auto
from json import JSONDecoder, JSONEncoder, JSONDecodeError
from typing import Optional


class IMockSerial:
    def write(self, contenu: bytes) -> None: ...
    def readline(self) -> bytes: ...
    def read_all(self) -> bytes: ...


class eMockType(Enum):
    """Type de Mock série"""
    CLI = auto
    TEST = auto
    MULTI_TEST = auto


class MockSerial(IMockSerial):
    """Représente une fausse communication par port série"""

    def __init__(self, type: eMockType = eMockType.TEST) -> None:
        """Initialise une réponse vide pour l'objet"""
        self.reponse = b'{"vide"}'
        self.requete = b'{"vide"}'
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()
        self.type = type

    def write(self, contenu: bytes) -> None:
        """Stocke une réponse à un message reçu ou ajoute le message à la queue"""
        if self.type is eMockType.CLI:
            print(f"\tMOCK_RECEIVE <- <{contenu}>")
        self.requete = contenu

        try:
            self.reponse = self.json_decoder.decode(contenu.decode('utf8'))
        except JSONDecodeError:
            if self.type is eMockType.CLI:
                print(f"ERREUR: JSON invalide -> {contenu.decode('utf8')}")
            self.reponse = b'{"erreur"}'
            return

        try:
            self.reponse["type"] = "ack"
        except KeyError:
            self.reponse = b'{"vide"}'
        else:
            self.reponse = bytes(self.json_encoder.encode(
                self.reponse), encoding='utf8')

    def readline(self) -> bytes:
        """Envoie la réponse stockée"""
        if self.type is eMockType.CLI:
            print(f"\tMOCK_SEND -> <{self.reponse}>")
        return self.reponse

    def read_all(self) -> bytes:
        """Envoie la réponse stockée"""
        return self.readline()


class DualMockSerial(IMockSerial):
    """Représente un mock série à deux canaux différents pour la lecture et l'écriture"""

    def __init__(self, canal_lecture: Optional[MockSerial] = None, canal_ecriture: Optional[MockSerial] = None) -> None:
        """Initialise un mock de connection série avec un mock différent pour la lecture et l'écriture"""
        self.lecture = canal_lecture if canal_lecture is not None else MockSerial(
            eMockType.TEST)
        self.ecriture = canal_ecriture if canal_lecture is not None else MockSerial(
            eMockType.TEST)

    def write(self, contenu: bytes) -> None:
        self.ecriture.write(contenu=contenu)

    def readline(self) -> bytes:
        return self.lecture.readline()

    def read_all(self) -> bytes:
        return self.lecture.read_all()
