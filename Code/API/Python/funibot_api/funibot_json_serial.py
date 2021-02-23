from json import encoder
from traceback import print_exc
from benedict import benedict
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
from enum import Enum
import time
from typing import Union, Tuple, List


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

FUNI_ERREUR_MAJ =\
    [
        False,  # 0
        True,   # 1
        True,   # 2
        True,   # 3
        True,   # 4
        True,   # 5
        False,  # 6
        False,  # 7
        True,   # 8
        True,   # 9
        False,  # 10
        True,   # 11
        False,  # 12
        True,   # 13
        False,  # 14
        True,   # 15
        True,   # 16
        True,   # 17
        True    # 18
    ]


class eFuniErreur(Enum):
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


class FuniErreur:
    """Représente une erreur du Funibot"""
    
    def __init__(self, erreur: Union[int, eFuniErreur], temps: int) -> None:
        if isinstance(erreur, int):
            erreur = eFuniErreur(erreur)
        self.erreur = erreur
        self.id = erreur.value
        self.maj = FUNI_ERREUR_MAJ[self.id]
        self.t = temps

    def __repr__(self) -> str:
        return f"FuniErreur<{self.t}>{'(M)' if self.maj else ''}[{self.erreur.value}:{self.erreur.name}]"


class MockSerial:

    def __init__(self):
        self.reponse = '{"vide"}'
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()

    def write(self, contenu):
        print(f"MOCK_RECEIVE -> <{contenu}>")
        try:
            self.reponse = self.json_decoder.decode(contenu.decode('utf8'))
            self.reponse = self.reponse
        except:
            print_exc()
            self.reponse = '{"erreur"}'
            return
        
        try:
            self.reponse["type"] = "ack"
        except KeyError:
            self.reponse = '{"vide"}'
        else:
            self.reponse = bytes(self.json_encoder.encode(self.reponse), encoding='utf8')

    def readline(self) -> str:
        print(f"MOCK_SEND -> <{self.reponse}>")
        return self.reponse


class FuniSerial():
    """Objet Serial possédant des méthodes pour envoyer et recevoir du JSON en lien avec le Funibot"""

    def __init__(self, serial: Union[Serial, MockSerial]):
        """Initialise le port série"""
        self.serial = serial
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()

    def envoyer(self, json: dict) -> Tuple[bool, str, dict]:
        """Envoie du json sous forme de dict"""
        self.serial.write(bytes(self.json_encoder.encode(json), encoding='utf8'))
        if json["type"] == FuniType.ACK.value:
            return (True, "ack", {})
        try:
            reponse = self.serial.readline()
            reponse = self.json_decoder.decode(reponse.decode("utf8"))
        except:
            print_exc()
            return (False, "erreur serial", {})

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
            raise TypeError("type n'est pas un FuniType")
        json = {}
        json["comm"] = "pot"
        json["type"] = type.value

        args = {}
        if not isinstance(id, int):
            raise TypeError("id n'est pas un entier")
            
        args["id"] = id
        if type is FuniType.SET:
            if position is None:
                raise ValueError("position est None")
            args["pos_x"] = position[0]
            args["pos_y"] = position[1]
            args["pos_z"] = position[2]
        else:
            args["pos_x"] = None
            args["pos_y"] = None
            args["pos_z"] = None

        json["args"] = args

        succes, message, retour = self.envoyer(json)
        if not succes:
            return message
        else:
            return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def cal(self, type: FuniType, mode: FuniModeCalibration, id: int, longueur: float) -> Union[str, float]:
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        if type == FuniType.GET:
            raise ValueError("GET n'est pas supporté")
        json = {}
        json["comm"] = "cal"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if not isinstance(id, int):
            raise TypeError("id n'est pas un entier")

        args["id"] = id
        if type is FuniType.SET:
            if longueur is None:
                raise ValueError("longueur est None")
            args["long"] = longueur
        else:
            args["long"] = None

        json["args"] = args

        succes, message, retour = self.envoyer(json)
        if not succes:
            return message
        else:
            return retour["args"]["long"]

    def pos(self, type: FuniType, position: Tuple[float, float, float] = None) -> Union[str, Tuple[float, float, float]]:
        if not isinstance(type, FuniType):
            raise TypeError("type n'est psa un FuniType")
        json = {}
        json["comm"] = "pos"
        json["type"] = type.value

        args = {}
        if type is FuniType.SET:
            if position is None:
                raise ValueError("position est None")
            args["pos_x"] = position[0]
            args["pos_y"] = position[1]
            args["pos_z"] = position[2]
        else:
            args["pos_x"] = None
            args["pos_y"] = None
            args["pos_z"] = None

        json["args"] = args

        try:
            succes, message, retour = self.envoyer(json)
        except:
            print_exc()
        
        if not succes:
            return message
        else:
            return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def dep(self, type: FuniType, mode: FuniModeDeplacement, direction: Tuple[float, float, float] = None) -> str:
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        if type == FuniType.GET:
            raise ValueError("GET n'est pas supporté")
        json = {}
        json["comm"] = "dep"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if type is FuniType.SET and \
                (mode == FuniModeDeplacement.DISTANCE or mode == FuniModeDeplacement.START):

            if direction is None:
                raise ValueError("direction est None")
            args["axe_x"] = direction[0]
            args["axe_y"] = direction[1]
            args["axe_z"] = direction[2]
        else:
            args["axe_x"] = None
            args["axe_y"] = None
            args["axe_z"] = None

        json["args"] = args

        succes, message, retour = self.envoyer(json)
        if not succes:
            return message
        else:
            return (retour["args"]["axe_x"], retour["args"]["axe_y"], retour["args"]["axe_z"])

    def err(self, type: FuniType, code: Union[None, int, eFuniErreur]=None, temps: int=None, err_sup: int=None) -> Tuple[List[FuniErreur], List[str]]:
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        if type == FuniType.SET:
            raise ValueError("SET n'est pas supporté")
        json = {}
        json["comm"] = "err"
        json["type"] = type.value

        if type == FuniType.GET:
            args = None
        else:
            args = {}
            
            if isinstance(code, eFuniErreur):
                code = code.value
            if not isinstance(code, int):
                raise TypeError("code n'est pas une eFuniErreur ou un entier")
            if code <= 0:
                raise ValueError("code est un entier négatif, il devrait être positif")

            if not isinstance(temps, int):
                raise TypeError("temps n'est pas un entier")

            if not isinstance(temps, int):
                raise TypeError("err_sup n'est pas un entier")
            if not err_sup >= 0:
                raise ValueError("err_sup est négatif")

            args["id"] = code
            args["maj"] = FUNI_ERREUR_MAJ[code]
            args["t"] = temps
            args["err_sup"] = err_sup

        json["args"] = args

        succes = True
        encore = True
        erreurs = []
        messages = []
        while succes and encore:
            succes, message, retour = self.envoyer(json)
            encore = (retour["args"]["err_sup"] > 0)
            
            if not succes:
                messages.append(message)
            else:
                erreurs.append(FuniErreur(retour["args"]["id"], retour["args"]["t"]))
        
        return (erreurs, messages)
