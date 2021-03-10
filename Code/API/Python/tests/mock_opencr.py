from __future__ import annotations
from json import JSONDecoder, JSONEncoder, JSONDecodeError
from queue import Empty
from funibot_api.funibot import Vecteur

from funibot_api.funibot_json_serial import FuniSerial, FuniType
from typing import Callable, Union, Tuple, Dict, Any, Optional
from threading import Thread, Event, Condition
from tests.mock_serial import MockSerial, MockType, DualMockSerial
from enum import Enum


class eGestionCommandesJSON(Enum):
    POT = 'pot',
    CAL = 'cal',
    POS = 'pos',
    DEP = 'dep',
    ERR = 'err',
    UNK = 'inconnu',
    PASSE = 'passe'


class CommandeInconnue(Exception):
    pass


class MockOpenCR(Thread):
    """Mock le OpenCR pour les tests"""

    def __init__(self, mock_serie: DualMockSerial) -> None:
        super().__init__(daemon=True)
        # self.mock_serial = mock
        self.var_cond = mock_serie.var_cond
        self.serial: FuniSerial = FuniSerial(mock_serie)
        self.poteaux = []
        self.position = Vecteur()
        self.json_decoder = JSONDecoder()
        self.arret = Event()
        self.name = self.__class__.__name__

    def arreter(self) -> None:
        self.arret.set()
        with self.var_cond:
            self.var_cond.notify_all()

    def pot(self, type: FuniType, json: Dict[str, Any]):
        pass

    def cal(self, type: FuniType, json: Dict[str, Any]):
        pass

    def pos(self, type: FuniType, json: Dict[str, Any]):
        pass

    def dep(self, type: FuniType, json: Dict[str, Any]):
        pass

    def err(self, type: FuniType, json: Dict[str, Any]):
        pass

    def inconnu(self, *_):
        raise CommandeInconnue

    def passe(self, *_):
        pass

    def run(self):
        if self.arret is None:
            while True:
                self.loop()
        else:
            continuer = True
            while continuer:
                continuer = self.loop()
            print("Fin du thread")
            return

    def loop(self) -> bool:
        with self.var_cond:
            print("pre-loop")
            self.var_cond.wait()
            print("Loop")
            try:
                json = self.serial.serial.readline()
            except Empty:
                pass
            else:
                commande, ftype, message = self._parser_entree_json(json=json)
                fonction: Callable[[FuniType, Dict[str, Any]],
                                None] = self.__getattribute__(commande.value)
                fonction(ftype, message)

        print(f"Quit: {self.arret.is_set()}")
        return not self.arret.is_set()

    def _parser_entree_json(self, json: bytes) -> Tuple[eGestionCommandesJSON, FuniType, Dict[str, Any]]:
        try:
            message = self.json_decoder.decode(json.decode('utf8'))
        except JSONDecodeError:
            return (eGestionCommandesJSON.UNK, FuniType.ACK, {})

        try:
            commande = eGestionCommandesJSON(message["comm"])
        except (KeyError, ValueError):
            return (eGestionCommandesJSON.UNK, FuniType.ACK, {})

        try:
            ftype = FuniType(message["type"])
        except (KeyError, ValueError):
            return (eGestionCommandesJSON.UNK, FuniType.ACK, {})

        if ftype is FuniType.ACK:
            return (eGestionCommandesJSON.PASSE, FuniType.ACK, {})
        else:
            return (commande, ftype, message)

    @staticmethod
    def _vec_vers_json(vec: Vecteur, axe_au_lieu_de_pos: bool = False) -> dict:
        prefixe = 'pos_'
        if axe_au_lieu_de_pos:
            prefixe = 'axe_'

        vec_dict = {}
        for axe in 'xyz':
            vec_dict[f"{prefixe}{axe}"] = vec.__getattribute__(axe)
        return vec_dict
