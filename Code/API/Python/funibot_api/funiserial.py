from __future__ import annotations

from traceback import print_exc
from benedict import benedict
from json import JSONDecoder, JSONEncoder, JSONDecodeError
from enum import Enum
from typing import Union, Tuple, List, Optional

from funibot_api.mock_serial import IMockSerial

from serial import Serial


class FuniType(Enum):
    """Type de communication (GET/SET/ACK)"""
    GET = 'get'
    SET = 'set'
    ACK = 'ack'


class FuniModeDeplacement(Enum):
    """Mode de déplacement pour 'dep' (START/STOP/DISTANCE)"""
    START = 'start'
    STOP = 'stop'
    DISTANCE = 'distance'


class FuniModeCalibration(Enum):
    """Mode de calibration pour 'cal' (CABLE/SOL)"""
    CABLE = 'cable'
    SOL = 'sol'


class FuniModeMoteur(Enum):
    """Mode de calibration pour 'mot' (ON/OFF/RESET)"""
    ON = 'on'
    OFF = 'off'
    RESET = 'reset'


class FuniCommException(Exception):
    """Exception lancée lors d'une erreur de communication ou de paramètres"""
    pass


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
        "GET_POLE_RELATIF_INEXISTANT",
        "POLES_CONFONDUES_2D",
        "POLES_CONFONDUES_3D",
        "SETUP_SECURITE_AVEC_MOINS_DE_3_POLES",
        "SECURITE_AVEC_MOINS_DE_3_POLES",
        "SORTIE_DE_ZONE_DE_SECURITE",

        # Doit rester la dernière pour avoir l'indice -1
        "ERREUR_INCONNUE"
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
        True,   # 18
        True,   # 19
        True,   # 20
        True,   # 21
        True,   # 22
        False,  # 23
    ]


class eFuniErreur(Enum):
    """Énumération des erreurs du OpenCR"""
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
    POLES_CONFONDUES_2D = 19
    POLES_CONFONDUES_3D = 20
    SETUP_SECURITE_AVEC_MOINS_DE_3_POLES = 21
    SECURITE_AVEC_MOINS_DE_3_POLES = 22
    SORTIE_DE_ZONE_DE_SECURITE = 23

    ERREUR_INCONNUE_VOIR_DICTIONNAIRE = -1


class FuniErreur:
    """Représente une erreur du Funibot"""

    def __init__(self, erreur: Union[int, eFuniErreur], temps: int, maj: bool) -> None:
        """Initialise une FuniErreur à partir de son eFuniErreur ou de son id"""
        if isinstance(erreur, int):
            self.id = erreur
            try:
                self.erreur = eFuniErreur(erreur)
            except ValueError:
                self.erreur = eFuniErreur(-1)
        else:
            self.id = erreur.value
            self.erreur = erreur
        self.maj = maj
        self.t = temps

    def __repr__(self) -> str:
        """Affiche une FuniErreur"""
        return f"FuniErreur<{self.t}>{'(M)' if self.maj else ''}[{self.id}:{self.erreur.name}]"


class FuniSerial():
    """Objet Serial possédant des méthodes pour envoyer et recevoir du JSON en lien avec le Funibot"""

    def __init__(self, serial: Union[Serial, IMockSerial]):
        """Initialise le port série"""
        self.serial = serial
        self.json_encoder = JSONEncoder()
        self.json_decoder = JSONDecoder()

    def __repr__(self):
        if isinstance(self.serial, Serial):
            return f"{self.serial.portstr}@{self.serial.baudrate}"
        else:
            return "Mock"

    def envoyer(self, json: dict) -> dict:
        """Envoie du json sous forme de dict"""
        self.serial.write(
            bytes(self.json_encoder.encode(json), encoding='utf8'))
        if json["type"] == FuniType.ACK.value:
            return {}

        try:
            reponse = self.serial.readline()
            reponse = self.json_decoder.decode(reponse.decode("utf8"))
        except JSONDecodeError:
            print_exc()
            raise FuniCommException("erreur serial lors du décodage")

        if reponse["type"] != FuniType.ACK.value:
            raise FuniCommException(
                f"{reponse['type']} au lieu de {FuniType.ACK.value}")

        try:
            self._valider_reponse(json_envoye=json, json_recu=reponse)
        except FuniCommException:
            raise

        return reponse

    @staticmethod
    def _valider_reponse(json_envoye: dict, json_recu: dict) -> None:
        """Compare les documents JSON envoyé et reçu pour valider que la communication a réussi"""
        json_envoye_flat: dict = benedict(json_envoye).flatten("/")
        json_recu_flat: dict = benedict(json_recu).flatten("/")

        for key, value in json_recu_flat.items():
            if not key in json_envoye_flat:
                raise FuniCommException(
                    f"{key} est présente dans la réponse mais pas dans le message d'origine")
            if key != "type" and json_envoye_flat[key] is not None and json_envoye_flat[key] != value:
                raise FuniCommException(
                    f"{key}: Reçu <{value}>, attendu <{json_envoye_flat[key]}>")
            elif key == "type" and json_envoye_flat[key] not in {"get", "set"}:
                raise FuniCommException(
                    f"type: Envoyé <{json_envoye_flat[key]}>, attendu <get | set>")

    def pot(self, type: FuniType, id: int, position: Tuple[float, float, float] = None) -> Optional[Tuple[float, float, float]]:
        """S'occupe de la communication série pour la commande JSON 'pot'"""
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        json = {}
        json["comm"] = "pot"
        json["type"] = type.value

        args = {}
        if not isinstance(id, int):
            raise TypeError("id n'est pas un entier")
        if id < 0:
            raise ValueError("id est inférieur à 0")

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

        try:
            retour = self.envoyer(json)
        except FuniCommException:
            print_exc()
            return None

        return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def cal(self, type: FuniType, mode: FuniModeCalibration, id: Optional[int] = None, longueur: Optional[float] = None) -> Optional[float]:
        """S'occupe de la communication série pour la commande JSON 'cal'"""
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")

        json = {}
        json["comm"] = "cal"
        json["type"] = type.value

        args = {}
        args["mode"] = mode.value
        if mode is not FuniModeCalibration.SOL:
            if not isinstance(id, int):
                raise TypeError("id n'est pas un entier")
            if id < 0:
                raise ValueError("id est inférieur à 0")
        else:
            id = None

        args["id"] = id
        if type is FuniType.SET:
            if longueur is None:
                raise ValueError("longueur est None")
            elif longueur < 0 and mode is not FuniModeCalibration.SOL:
                raise ValueError("longueur est inférieure à zéro")
            args["long"] = longueur
        else:
            args["long"] = None

        json["args"] = args

        try:
            retour = self.envoyer(json)
        except FuniCommException:
            print_exc()
            return None

        return retour["args"]["long"]

    def pos(self, type: FuniType, position: Tuple[float, float, float] = None) -> Optional[Tuple[float, float, float]]:
        """S'occupe de la communication série pour la commande JSON 'pos'"""
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
            retour = self.envoyer(json)
        except FuniCommException as e:
            print_exc()
            return None

        return (retour["args"]["pos_x"], retour["args"]["pos_y"], retour["args"]["pos_z"])

    def dep(self, type: FuniType, mode: FuniModeDeplacement, direction: Tuple[float, float, float] = None) -> Optional[Tuple[float, float, float]]:
        """S'occupe de la communication série pour la commande JSON 'dep'"""
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

        try:
            retour = self.envoyer(json)
        except FuniCommException:
            print_exc()
            return None

        return (retour["args"]["axe_x"], retour["args"]["axe_y"], retour["args"]["axe_z"])

    def err(self, type: FuniType, code: Union[None, int, eFuniErreur] = None, temps: int = None, err_sup: int = None) -> List[FuniErreur]:
        """S'occupe de la communication série pour la commande JSON 'err'"""
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        if type == FuniType.SET:
            raise ValueError("SET n'est pas supporté")
        json = {}
        json["comm"] = "err"
        json["type"] = type.value

        if type == FuniType.GET:
            args = {}
            args["id"] = None
            args["maj"] = None
            args["t"] = None
            args["err_sup"] = None
        else:
            args = {}

            if isinstance(code, eFuniErreur):
                code = code.value
            if not isinstance(code, int):
                raise TypeError("code n'est pas une eFuniErreur ou un entier")
            if code <= 0:
                raise ValueError(
                    "code est un entier négatif, il devrait être positif")

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

        encore = True
        erreurs = []
        err_limite = 10

        while encore:
            try:
                retour = self.envoyer(json)
            except FuniCommException:
                print_exc()
                err_limite -= 1
                if err_limite == 0:
                    break
                else:
                    continue

            try:
                encore = (retour["args"]["err_sup"] > 0)
            except KeyError:
                print_exc()
                break

            erreurs.append(FuniErreur(
                retour["args"]["id"], retour["args"]["t"], retour["args"]["maj"]))

        return erreurs
    
    def log(self, type: FuniType, msg: str = None) -> Optional[str]:
        """S'occupe de la communication série pour la commande JSON 'log'"""
        if not isinstance(type, FuniType):
            raise TypeError("type n'est pas un FuniType")
        if type == FuniType.SET:
            raise ValueError("SET n'est pas supporté")
        json = {}
        json["comm"] = "log"
        json["type"] = type.value

        if type == FuniType.GET:
            args = {}
            args["msg"] = None
        else:
            args = {}
            args["msg"] = msg

        json["args"] = args

        try:
            retour = self.envoyer(json)
        except FuniCommException:
            print_exc()
            return None

        msg_retour: str = retour["args"]["msg"] if retour["args"]["msg"] is not None else ""
        msg_retour = msg_retour if msg_retour != "" else "__vide__"
        msg_retour = msg_retour.replace('\r', '\n')
        return msg_retour

    def mot(self, type: FuniType, mode: Optional[FuniModeMoteur] = None) -> Optional[FuniModeMoteur]:
        """S'occupe de la communication série pour la commande JSON 'mot'"""
        if not isinstance(type, FuniType):
            raise TypeError("type n'est psa un FuniType")
        json = {}
        json["comm"] = "mot"
        json["type"] = type.value

        args = {}
        if type is not FuniType.GET:
            if mode is None:
                raise ValueError("mode est None")
            args["mode"] = mode.value
        else:
            args["mode"] = None

        json["args"] = args

        try:
            retour = self.envoyer(json)
        except FuniCommException as e:
            print_exc()
            return None
        try:
            return FuniModeMoteur(retour["args"]["mode"])
        except ValueError:
            return None