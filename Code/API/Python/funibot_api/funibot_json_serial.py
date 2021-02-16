import benedict
from serial import Serial
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from benedict import benedict
from enum import Enum
from typing import Union


class FuniType(Enum):
    GET = 'get'
    SET = 'set'
    ACK = 'ack'


class FuniModeDeplacement(Enum):
    START = 'start'
    STOP = 'stop'
    DISTANCE = 'distance'


class FuniErreur(Enum):
    pass


class FuniSerial(Serial):
    """Objet Serial possédant des méthodes pour envoyer et recevoir du JSON en lien avec le Funibot"""

    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout, xonxoff,
                 rtscts, write_timeout, dsrdtr, inter_byte_timeout, exclusive, **kwargs):
        """Initialise le port série"""
        super().__init__(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity,
                         stopbits=stopbits, timeout=timeout, xonxoff=xonxoff, rtscts=rtscts,
                         write_timeout=write_timeout, dsrdtr=dsrdtr,
                         inter_byte_timeout=inter_byte_timeout, exclusive=exclusive, **kwargs)

        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()

    def envoyer(self, json: dict) -> tuple(bool, str, dict):
        """Envoie du json sous forme de dict"""
        self.write(bytes(self.json_encoder.encode(json)))
        reponse = self.json_decoder.decode(self.readline())

        if json["type"] == "set" and reponse["type"] == "ack":
            return self._valider_reponse(json_envoye=json, json_recu=reponse)
        else:
            return (False, f"{reponse['type']} au lieu de 'ack'", reponse)

    @staticmethod
    def _valider_reponse(json_envoye: dict, json_recu: dict) -> tuple(bool, str):
        json_envoye_flat = benedict(json_envoye).flatten()
        json_recu_flat = benedict(json_recu).flatten()

        for key, value in json_recu_flat.items():
            if not key in json_envoye_flat:
                return (False, key, json_recu)
            if key != "type" and json_envoye_flat[key] is not None and json_envoye_flat[key] != value:
                return (False, f"{key}: {value}", json_recu)

        return (True, "")

    def pot(self, type: FuniType, id: int, position: tuple(float, float, float) = None) -> Union[str, float(float, float, float)]:
        json = {}
        json["com"] = "pot"
        json["type"] = type.value

        args = {}
        args["id"] = id
        if type is FuniType.SET:
            if position is None:
                return None
            args["pos_x"] = position(0)
            args["pos_y"] = position(1)
            args["pos_z"] = position(2)
        else:
            args["pos_x"] = None
            args["pos_y"] = None
            args["pos_z"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def pos(self, type: FuniType, position: tuple(float, float, float) = None) -> Union[str, float(float, float, float)]:
        json = {}
        json["com"] = "pos"
        json["type"] = type.value

        args = {}
        if type is FuniType.SET:
            if position is None:
                return None
            args["pos_x"] = position(0)
            args["pos_y"] = position(1)
            args["pos_z"] = position(2)
        else:
            args["pos_x"] = None
            args["pos_y"] = None
            args["pos_z"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def dep(self, type: FuniType, mode: FuniModeDeplacement, direction: tuple(float, float, float) = None) -> str:
        json = {}
        json["com"] = "dep"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if type is FuniType.SET and \
                (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

            if direction is None:
                return None
            args["axe_x"] = direction(0)
            args["axe_y"] = direction(1)
            args["axe_z"] = direction(2)
        else:
            args["axe_x"] = None
            args["axe_y"] = None
            args["axe_z"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return ""

    def err(self, type: FuniType, code: Union[None, FuniErreur], direction: tuple(float, float, float) = None) -> str:
        json = {}
        json["com"] = "err"
        json["type"] = type.value

        args = {}
        args["code"] = None if code is None else code.value
        if type is FuniType.SET and \
                (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

            if direction is None:
                return None
            args["axe_x"] = direction(0)
            args["axe_y"] = direction(1)
            args["axe_z"] = direction(2)
        else:
            args["axe_x"] = None
            args["axe_y"] = None
            args["axe_z"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return ""
