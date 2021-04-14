from __future__ import annotations

from enum import Enum, auto
from json import JSONDecoder, JSONEncoder, JSONDecodeError
from typing import Optional


class IMockSerial:
    def write(self, contenu: bytes) -> None: ...
    def readline(self) -> bytes: ...
    def read_all(self) -> bytes: ...
    def reset_input_buffer(self) -> None: ...

    @property
    def timeout(self) -> float: return 0
    @timeout.setter
    def timeout(self, val) -> None: pass


class eMockType(Enum):
    """Type de Mock série"""
    CLI = auto()
    TEST = auto()
    MULTI_TEST = auto()


class MockSerial(IMockSerial):
    """Représente une fausse communication par port série"""

    def __init__(self, type: eMockType = eMockType.TEST) -> None:
        """Initialise une réponse vide pour l'objet"""
        self.reponse = b'{"vide"}'
        self.requete = b'{"vide"}'
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()
        self.type = type
        if self.type is eMockType.MULTI_TEST:
            self.reponses = []
            self.requetes = []
            self.clear_requetes = lambda: self.requetes.clear()
            self.clear_reponses = lambda: self.reponses.clear()
            self.clear = lambda: self.clear_reponses(), self.clear_requetes()

    def write(self, contenu: bytes) -> None:
        """Stocke une réponse à un message reçu ou ajoute le message à la queue"""
        if self.type is eMockType.CLI:
            print(f"\tMOCK_RECEIVE <- <{contenu}>")
        self.requete = contenu
        if self.type is eMockType.MULTI_TEST:
            self.requetes.append(self.requete)

        try:
            self.reponse = self.json_decoder.decode(contenu.decode('utf8'))
        except JSONDecodeError:
            if self.type is eMockType.CLI:
                print(f"ERREUR: JSON invalide -> {contenu.decode('utf8')}")
            self.reponse = b'{"erreur"}'
            if self.type is eMockType.MULTI_TEST:
                self.reponses.append(self.reponse)
            return

        try:
            self.reponse["type"] = "ack"
        except KeyError:
            self.reponse = b'{"vide"}'
        else:
            self.reponse = bytes(self.json_encoder.encode(
                self.reponse), encoding='utf8')

        if self.type is eMockType.MULTI_TEST:
            self.reponses.append(self.reponse)

    def readline(self) -> bytes:
        """Envoie la réponse stockée"""
        if self.type is eMockType.CLI:
            print(f"\tMOCK_SEND -> <{self.reponse}>")
        if self.type is not eMockType.MULTI_TEST:
            return self.reponse
        else:
            try:
                reponse = self.reponses.pop(0)
                return reponse
            except IndexError:
                return b'{"liste_vide"}'

    def read_all(self) -> bytes:
        """Envoie la réponse stockée"""
        return self.readline()

    def reset_input_buffer(self) -> None:
        self.reponse = b'{"vide"}'
        if self.type is eMockType.MULTI_TEST:
            return self.reponses.clear()


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
