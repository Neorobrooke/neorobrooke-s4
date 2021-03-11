from __future__ import annotations

from enum import Enum, auto
from queue import Queue, Empty
from json import JSONDecoder, JSONEncoder, JSONDecodeError
from threading import Condition
from typing import Optional


class IMockSerial:
    def write(self, contenu: bytes) -> None: ...
    def readline(self) -> bytes: ...
    def read_all(self) -> bytes: ...


class MockType(Enum):
    """Type de Mock série"""
    CLI = auto,
    TEST = auto


class MockSerial(IMockSerial):
    """Représente une fausse communication par port série"""

    def __init__(self, type: MockType = MockType.TEST, timeout: float = 2) -> None:
        """Initialise une réponse vide pour l'objet"""
        self.reponse = b'{"vide"}'
        self.requete = b'{"vide"}'
        self.buffer = Queue()
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()
        self.is_cli = (type is MockType.CLI)
        self.timeout = timeout

    def write(self, contenu: bytes) -> None:
        """Stocke une réponse à un message reçu ou ajoute le message à la queue"""
        if self.is_cli:
            print(f"MOCK_RECEIVE <- <{contenu}>")
            self.requete = contenu

            try:
                self.reponse = self.json_decoder.decode(contenu.decode('utf8'))
            except JSONDecodeError:
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
        else:
            for elem in self.reponse.strip().split(b'\n'):
                self.buffer.put(elem)

    def readline(self) -> bytes:
        """Envoie la réponse stockée ou envoie le premier message de la queue"""
        if self.is_cli:
            print(f"MOCK_SEND -> <{self.reponse}>")
            return self.reponse
        else:
            try:
                valeur = self.buffer.get(timeout=self.timeout)
            except Empty:
                raise
            self.buffer.task_done()
            return valeur

    def read_all(self) -> bytes:
        """Envoie la réponse stockée"""
        if self.is_cli:
            return self.readline()
        else:
            liste = []
            try:
                while True:
                    valeur = self.buffer.get_nowait()
                    self.buffer.task_done()
                    liste.append(valeur)
            except Empty:
                if len(liste) == 0:
                    return b'{"vide"}'
                else:
                    return b'\n'.join(liste)


class DualMockSerial(IMockSerial):
    """Représente un mock série à deux canaux différents pour la lecture et l'écriture"""

    def __init__(self, canal_lecture: Optional[MockSerial] = None, canal_ecriture: Optional[MockSerial] = None, timeout: float = 2) -> None:
        """Initialise un mock de connection série avec un mock différent pour la lecture et l'écriture"""
        self.lecture = canal_lecture if canal_lecture is not None else MockSerial(MockType.TEST, timeout=timeout)
        self.ecriture = canal_ecriture if canal_lecture is not None else MockSerial(MockType.TEST, timeout=timeout)
        self.var_cond = Condition()

    def write(self, contenu: bytes) -> None:
        with self.var_cond:
            try:
                self.ecriture.write(contenu=contenu)
            except Empty:
                raise
            self.var_cond.notify()

    def readline(self) -> bytes:
        return self.lecture.readline()

    def read_all(self) -> bytes:
        return self.lecture.read_all()
