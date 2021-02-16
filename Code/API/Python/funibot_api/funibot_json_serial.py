import benedict
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from benedict import benedict
from enum import Enum
from typing import Union, Tuple


from serial import Serial


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

class MockSerial:

    def write(self, contenu):
        print(contenu)
    
    def readline(self) -> str:
        ligne = input()
        return ligne

class FuniSerial():
    """Objet Serial possédant des méthodes pour envoyer et recevoir du JSON en lien avec le Funibot"""

    def __init__(self, serial: Union[Serial, MockSerial]):
        """Initialise le port série"""
        self.serial = serial
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()

    def envoyer(self, json: dict) -> Tuple[bool, str, dict]:
        """Envoie du json sous forme de dict"""
        self.serial.write(self.json_encoder.encode(json))
        reponse = self.json_decoder.decode(self.serial.readline())

        if json["type"] == "set" and reponse["type"] == "ack":
            return self._valider_reponse(json_envoye=json, json_recu=reponse)
        else:
            return (False, f"{reponse['type']} au lieu de 'ack'", reponse)

    @staticmethod
    def _valider_reponse(json_envoye: dict, json_recu: dict) -> Tuple[bool, str]:
        json_envoye_flat = benedict(json_envoye).flatten()
        json_recu_flat = benedict(json_recu).flatten()

        for key, value in json_recu_flat.items():
            if not key in json_envoye_flat:
                return (False, key, json_recu)
            if key != "type" and json_envoye_flat[key] is not None and json_envoye_flat[key] != value:
                return (False, f"{key}: {value}", json_recu)

        return (True, "")

    def pot(self, type: FuniType, id: int, position: Tuple[float, float, float] = None) -> Union[str, Tuple[float, float, float]]:
        json = {}
        json["comm"] = "pot"
        json["type"] = type.value

        args = {}
        args["id"] = id
        if type is FuniType.SET:
            if position is None:
                return None
            args["pos_x"] = position[0]
            args["pos_y"] = position[1]
            args["pos_z"] = position[2]
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

    def pos(self, type: FuniType, position: Tuple[float, float, float] = None) -> Union[str, Tuple[float, float, float]]:
        json = {}
        json["comm"] = "pos"
        json["type"] = type.value

        args = {}
        if type is FuniType.SET:
            if position is None:
                return None
            args["pos_x"] = position[0]
            args["pos_y"] = position[1]
            args["pos_z"] = position[2]
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

    def dep(self, type: FuniType, mode: FuniModeDeplacement, direction: Tuple[float, float, float] = None) -> str:
        json = {}
        json["comm"] = "dep"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if type is FuniType.SET and \
                (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

            if direction is None:
                return None
            args["axe_x"] = direction[0]
            args["axe_y"] = direction[1]
            args["axe_z"] = direction[2]
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

    def err(self, type: FuniType, code: Union[None, FuniErreur], direction: Tuple[float, float, float] = None) -> str:
        pass
        # json = {}
        # json["comm"] = "err"
        # json["type"] = type.value

        # args = {}
        # args["code"] = None if code is None else code.value
        # if type is FuniType.SET and \
        #         (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

        #     if direction is None:
        #         return None
        #     args["axe_x"] = direction(0)
        #     args["axe_y"] = direction(1)
        #     args["axe_z"] = direction(2)
        # else:
        #     args["axe_x"] = None
        #     args["axe_y"] = None
        #     args["axe_z"] = None

        # json["args"] = args

        # success, message, retour = self.envoyer(json)
        # if not success:
        #     return message
        # else:
        #     return ""
