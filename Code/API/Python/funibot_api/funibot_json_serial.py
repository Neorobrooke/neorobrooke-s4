from benedict import benedict
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
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


class FuniModeCalibration(Enum):
    CABLE = 'cable'


FUNI_ERREUR_MESSAGES =\
    [
        "AUCUNE_ERREUR",
        "ADD_POLE_DEPASSEMENT",
        "SET_POLE_INEXISTANT",
        "SET_LONGUEUR_CABLE_INEXISTANT",
        "GET_POSITION_PAS_DE_POLES",
        "GET_POSITION_TROP_COURTS_2D",
        "GET_POSITION_0_TROP_LONG_2D",
        "GET_POSITION_1_TROP_LONG_2D",
        "GET_POSITION_TROP_COURTS_3D",
        "GET_POSITION_ALIGNES_3D",
        "GET_POSITION_RACINE_ESTIMEE_3D",
        "DEPLACEMENT_DIRECTIONNEL_ERREUR_MAJEURE",
        "DEPLACEMENT_DIRECTIONNEL_ERREUR_MINEURE",
        "DEPLACEMENT_POSITION_ERREUR_MAJEURE",
        "DEPLACEMENT_POSITION_ERREUR_MINEURE",
        "GET_POLE_INEXISTANT",
        "GET_ACCROCHE_INEXISTANTE",
        "GET_LONGUEUR_CABLE_INEXISTANT",
        "GET_POLE_RELATIF_INEXISTANT"
    ]


class FuniErreur(Enum):
    AUCUNE_ERREUR = 0
    ADD_POLE_DEPASSEMENT = 1
    SET_POLE_INEXISTANT = 2
    SET_LONGUEUR_CABLE_INEXISTANT = 3
    GET_POSITION_PAS_DE_POLES = 4
    GET_POSITION_TROP_COURTS_2D = 5
    GET_POSITION_0_TROP_LONG_2D = 6
    GET_POSITION_1_TROP_LONG_2D = 7
    GET_POSITION_TROP_COURTS_3D = 8
    GET_POSITION_ALIGNES_3D = 9
    GET_POSITION_RACINE_ESTIMEE_3D = 10
    DEPLACEMENT_DIRECTIONNEL_ERREUR_MAJEURE = 11
    DEPLACEMENT_DIRECTIONNEL_ERREUR_MINEURE = 12
    DEPLACEMENT_POSITION_ERREUR_MAJEURE = 13
    DEPLACEMENT_POSITION_ERREUR_MINEURE = 14
    GET_POLE_INEXISTANT = 15
    GET_ACCROCHE_INEXISTANTE = 16
    GET_LONGUEUR_CABLE_INEXISTANT = 17
    GET_POLE_RELATIF_INEXISTANT = 18


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
        if json["type"] == FuniType.ACK.value:
            return (True, "ack", {})
        reponse = self.json_decoder.decode(self.serial.readline())

        if json["type"] == "set" and reponse["type"] == "ack":
            return self._valider_reponse(json_envoye=json, json_recu=reponse)
        elif json["type"] == "get" and reponse["type"] == "ack":
            return(True, "", reponse)
        else:
            return (False, f"{reponse['type']} au lieu de 'ack'", reponse)

    @staticmethod
    def _valider_reponse(json_envoye: dict, json_recu: dict) -> Tuple[bool, str]:
        json_envoye_flat = benedict(json_envoye).flatten("/")
        json_recu_flat = benedict(json_recu).flatten("/")

        for key, value in json_recu_flat.items():
            if not key in json_envoye_flat:
                return (False, key, json_recu)
            if key != "type" and json_envoye_flat[key] is not None and json_envoye_flat[key] != value:
                return (False, f"{key}: {value}", json_recu)

        return (True, "", json_recu)

    def pot(self, type: FuniType, id: int, position: Tuple[float, float, float] = None) -> Union[str, Tuple[float, float, float]]:
        if not isinstance(type, FuniType):
            return "type n'est pas un FuniType"
        json = {}
        json["comm"] = "pot"
        json["type"] = type.value

        args = {}
        if not isinstance(id, int):
            return "id n'est pas un entier"

        args["id"] = id
        if type is FuniType.SET:
            if position is None:
                return "position est None"
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

    def cal(self, type: FuniType, mode: FuniModeCalibration, id: int, longueur: float) -> Union[str, float]:
        if not isinstance(type, FuniType):
            return "type n'est pas un FuniType"
        if type == FuniType.GET:
            return "GET pas supporté"
        json = {}
        json["comm"] = "cal"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if not isinstance(id, int):
            return "id n'est pas un entier"

        args["id"] = id
        if type is FuniType.SET:
            if longueur is None:
                return "longueur est None"
            args["long"] = longueur
        else:
            args["long"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return retour["args"]["long"]

    def pos(self, type: FuniType, position: Tuple[float, float, float] = None) -> Union[str, Tuple[float, float, float]]:
        if not isinstance(type, FuniType):
            return "type n'est pas un FuniType"
        json = {}
        json["comm"] = "pos"
        json["type"] = type.value

        args = {}
        if type is FuniType.SET:
            if position is None:
                return "position est None"
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
        if not isinstance(type, FuniType):
            return "type n'est pas un FuniType"
        if type == FuniType.GET:
            return "GET pas supporté"
        json = {}
        json["comm"] = "dep"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if type is FuniType.SET and \
                (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

            if direction is None:
                return "Pas de direction"
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

    def err(self, type: FuniType, code: Union[None, FuniErreur], flag: bool, msg: str = None, num: int = None)\
            -> Union[str, Tuple[Tuple[FuniErreur, bool, str], int]]:
        if not isinstance(type, FuniType):
            return "type n'est pas un FuniType"
        pass
        json = {}
        json["comm"] = "err"
        json["type"] = type.value

        args = {}
        args["code"] = None if code is None else code.value
        if type is FuniType.SET:
            if flag is None:
                return "flag est None"
            args["flag"] = flag
        else:
            args["flag"] = None

        if type is FuniType.ACK:
            args["msg"] = msg
            args["num"] = num
        else:
            args["msg"] = None
            args["num"] = None

        json["args"] = args

        success, message, retour = self.envoyer(json)
        if not success:
            return message
        else:
            return ((FuniErreur(retour["args"]["code"]), retour["args"]["flag"], retour["args"]["msg"]), retour["args"]["num"] - 1)
