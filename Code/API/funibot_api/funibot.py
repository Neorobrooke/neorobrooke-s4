from __future__ import annotations

from traceback import print_exc
from typing import Callable, ItemsView, Iterator, KeysView, List, ValuesView, Union, Optional
from pathlib import Path
from contextlib import contextmanager
from functools import wraps

from funibot_api.funiserial import (ErrSupEstNone, FuniErreur, eFuniErreur,
                                    eFuniModeCalibration, eFuniModeDeplacement,
                                    eFuniModeMoteur, FuniSerial, eFuniRegime,
                                    eFuniType, FuniCommException)
from funibot_api.funiconfig import FuniConfig
from funibot_api.funilib import Poteau, Vecteur, Direction, eRetourAttendre, sEntreeAttendre
from funibot_api.funipersistance import FuniPersistance, ErreurDonneesIncompatibles


class ErreurPersistance(ErreurDonneesIncompatibles):
    def __init__(self, bot: Funibot, *args: object) -> None:
        super().__init__(*args)
        self.bot = bot


def attendre_si_besoin(func) -> Callable:
    """La méthode attend la fin de son déplacement si on est dans un contextmanager tout_attendre."""
    @wraps(func)
    def wrapper(self: Funibot, *args, **kwargs):
        retour = func(self, *args, **kwargs)

        if self._attendre is not None:
            entree = sEntreeAttendre(nom_methode=func.__name__,
                                     retour_attendre=self.attendre())
            self._attendre.append(entree)

        return retour

    return wrapper


class Funibot:
    """Représente le Funibot"""

    def __init__(self, serial: FuniSerial, config: FuniConfig) -> None:
        """Initialise un Funibot.
           Peut lever une ErreurPersistance si la calibration automatique est active, mais échoue.
           Dans ce cas, l'objet est accessible via l'attribut 'bot' de l'exception.
        """
        self.serial = serial
        self.poteaux = Funibot._poteaux_liste_a_dict(config.liste_poteaux)
        self._initialiser_poteaux()
        self.sol = config.sol
        self._attendre: Optional[List[sEntreeAttendre]] = None

        self._initialiser_persistance(
            fichier=config.persistance,
            auto_persistance=config.auto_persistance,
            auto_calibration=config.auto_calibration)

        self.config = config

        if self.auto_calibration:
            try:
                self.calibrer()
            except ErreurDonneesIncompatibles as e:
                raise ErreurPersistance(
                    self, f"Erreur de calibration automatique: {e}")

    def __del__(self):
        if self.auto_persistance:
            try:
                self.enregister_calibration()
            except ErreurDonneesIncompatibles:
                pass

    @property
    def pos(self) -> Optional[Vecteur]:
        """Retourne la position actuelle du Funibot.
           Nécessite une communication série.
        """
        valeur = self.serial.pos(eFuniType.GET)
        if valeur is None:
            return None
        return Vecteur(*valeur)

    @pos.setter
    @attendre_si_besoin
    def pos(self, position: Vecteur) -> None:
        """Déplace le Funibot à la posision vectorielle demandée.
           Nécessite une communication série.
        """
        self.serial.pos(eFuniType.SET, position.vers_tuple())

    @property
    def sol(self) -> Optional[float]:
        """Retourne la position du sol.
           Nécessite une communication série.
        """
        return self.serial.cal(eFuniType.GET, eFuniModeCalibration.SOL)

    @sol.setter
    def sol(self, position: Optional[float]) -> None:
        """Change la position du sol.
           Nécessite une communication série.
        """
        self.serial.cal(
            eFuniType.SET, eFuniModeCalibration.SOL, longueur=position)

    def __getitem__(self, nom: str) -> Poteau:
        """Retourne le poteau ayant le nom demandé"""
        return self.poteaux[nom]

    def keys(self) -> KeysView[str]:
        """Retourne une vue sur les clés du dict des poteaux"""
        return self.poteaux.keys()

    def values(self) -> ValuesView[Poteau]:
        """Retourne une vue sur les valeurs du dict des poteaux"""
        return self.poteaux.values()

    def items(self) -> ItemsView[str, Poteau]:
        """Retourne une vue sur les items du dict des poteaux"""
        return self.poteaux.items()

    def __iter__(self) -> Iterator[Poteau]:
        """Retourne un générateur pour itérer sur les poteaux du funibot"""
        return (key for key in self.poteaux.values())

    def __repr__(self) -> str:
        """Représente le Funibot sous la forme Funibot[port_serie](poteaux)"""
        return f"Funibot[{self.serial}]({list(self.poteaux.values())})"

    @attendre_si_besoin
    def deplacer(self, direction: Union[Direction, Vecteur, str], distance: float = None) -> None:
        """Déplace le Funibot dans la direction indiquée par 'direction'.
           Si 'distance' n'est pas None, arrête après avoir parcouru 'distance'.
           Si 'distance' est la valeur spéciale 0, arrête après avoir parcouru la distance correspondant à la norme du vecteur
           Sinon, arrête avec un appel à 'stop'
           Nécessite une communication série.
        """
        if isinstance(direction, str):
            direction = Direction(direction=direction)

        if isinstance(direction, Direction):
            direction = direction.vecteur()

        mode = eFuniModeDeplacement.START if distance is None else eFuniModeDeplacement.DISTANCE

        if distance is not None and distance != 0:
            direction.norme = distance

        self.serial.dep(type=eFuniType.SET, mode=mode,
                        direction=direction.vers_tuple())
        return None

    def stop(self) -> None:
        """Arrête le mouvement du robot.
           Nécessite une communication série.
        """
        self.serial.dep(type=eFuniType.SET, mode=eFuniModeDeplacement.STOP)
        return None

    def erreur(self) -> Optional[List[FuniErreur]]:
        """Retourne la liste des erreurs.
           Nécessite une communication série.
        """
        try:
            erreurs = self.serial.err(eFuniType.GET)
            return erreurs
        except ErrSupEstNone as e:
            raise
        except Exception:
            print_exc()
            return None

    def log(self) -> Optional[str]:
        """Retourne tous les messages de déboguage.
           Nécessite une communication série.
        """
        try:
            msg = self.serial.log(eFuniType.GET)
            return msg
        except FuniCommException:
            return None

    @property
    def moteurs_actifs(self) -> Optional[bool]:
        """Retourne si les moteurs sont activés ou non.
           Nécessite une communication série.
        """
        valeur = self.serial.mot(eFuniType.GET)
        if valeur is eFuniModeMoteur.ON:
            return True
        elif valeur is eFuniModeMoteur.OFF:
            return False
        else:
            return None

    @moteurs_actifs.setter
    def moteurs_actifs(self, mode: bool):
        """Active ou désactive les moteurs.
           Nécessite une communication série.
        """
        actifs = eFuniModeMoteur.ON if mode is True else eFuniModeMoteur.OFF
        self.serial.mot(eFuniType.SET, actifs)

    def reinitialiser_moteurs(self):
        """Réinitialise les moteurs.
           Nécessite une communication série.
        """
        self.serial.mot(eFuniType.SET, eFuniModeMoteur.RESET)

    @property
    def arrete(self) -> bool:
        """Retourne un booléen qui vaut True si le robot est arrêté.
           Nécessite une communication série.
        """
        return self.serial.reg(eFuniType.GET) is eFuniRegime.ARRET

    @property
    def en_deplacement(self) -> bool:
        """Retourne un booléen qui vaut True si le robot est en mouvement.
           Nécessite une communication série.
        """
        regime = self.serial.reg(eFuniType.GET)
        return regime is eFuniRegime.DIRECTION or regime is eFuniRegime.POSITION

    @property
    def regime(self) -> Optional[eFuniRegime]:
        """Retourne le régime du Funibot sous forme d'un eFuniRegime.
           Valeurs:
                ARRETE s'il ne bouge pas
                DIRECTION s'il se déplace en direction sans condition d'arrêt (il attend un stop)
                POSITION s'il se déplace en position ou en direction d'une certaine distance
           Nécessite une communication série.
        """
        return self.serial.reg(eFuniType.GET)

    @property
    def duree_estimee(self) -> Optional[float]:
        """Retourne la durée estimée restante au déplacement en cours.
           Si regime != eFuniRegime.POSITION, retourne 0.
           Nécessite une communication série.
        """
        return self.serial.dur(eFuniType.GET)

    def attendre(self) -> eRetourAttendre:
        """Attend la fin du déplacement du Funibot.
           Retoune immédiatemment si le robot ne bouge pas.
           Si le robot est en déplacement, bloque l'exécution jusqu'à ce qu'il arrive s'arrête.
           Nécessite une communication série.
        """
        retour_1 = self.serial.att(eFuniType.SET, fin=False)
        if retour_1 is None:
            return eRetourAttendre.ERREUR_COMM
        elif retour_1[0] is False:
            return eRetourAttendre.ATTENTE_INVALIDE

        # Bloque l'exécution ici:
        timeout, self.serial.serial.timeout = self.serial.serial.timeout, None
        retour_2 = self.serial.att(eFuniType.SET, fin=True)
        self.serial.serial.timeout = timeout
        # Reprend l'exécution quand le Funibot arrête de se déplacer

        if retour_2 is None:
            return eRetourAttendre.ERREUR_COMM
        elif retour_2[0] is False:
            return eRetourAttendre.ARRET_INVALIDE
        else:
            return eRetourAttendre.OK

    @contextmanager
    def tout_attendre(self):
        self._attendre = list()
        try:
            yield self._attendre
        finally:
            self._attendre = None

    def repr_sol(self):
        """Retourne une représentation du sol"""
        return f"Sol -> {self.sol}"

    def enregister_calibration(self) -> None:
        """Enregistre la longueur des câbles dans un fichier de persistance"""
        try:
            self.persistance.enregistrer(
                self._poteaux_config(), self._longueur_cables())
        except AttributeError:
            print(
                "Impossible d'enregistrer la calibration: aucun fichier de persistance valide fourni.")
        except ErreurDonneesIncompatibles as e:
            print("Impossible d'enregistrer", end=': ')
            print(e)

    def calibrer(self):
        """Lit le fichier de persistance et calibre en conséquence"""
        try:
            for cle, longueur in self.persistance.calibrer(self._poteaux_config()).items():
                self.poteaux[cle].longueur_cable = longueur
        except AttributeError:
            print("Impossible de calibrer: aucun fichier de persistance valide fourni.")

    def _poteaux_config(self) -> List[dict]:
        """Génère une liste de dictionnaires pour les pôteaux.
           Même format que les fichiers de configuration et de persistance.
        """
        poteaux = []
        for poteau in self.poteaux.values():
            pole = {"x": poteau.pos_pole.x,
                    "y": poteau.pos_pole.y, "z": poteau.pos_pole.z}
            accroche = {"x": poteau.pos_acccroche.x,
                        "y": poteau.pos_acccroche.y, "z": poteau.pos_acccroche.z}
            dict_poteau = {poteau.nom: {"poles": pole, "accroches": accroche}}
            poteaux.append(dict_poteau)
        return poteaux

    def _longueur_cables(self) -> List[float]:
        """Génère une liste des longueurs des câbles.
           Même ordre que la liste de pôteaux provenant de _poteaux_config.
        """
        longueurs = []
        for poteau in self.poteaux.values():
            longueurs.append(poteau.longueur_cable)
        return longueurs

    def _initialiser_poteaux(self):
        """Donne un ID et assigne l'objet serial à chaque poteau"""
        self.poteaux_id: List[Poteau] = []
        for poteau in self.poteaux.values():
            poteau.init_poteau(
                id=len(self.poteaux_id), comm_serie=self.serial)
            self.poteaux_id.append(poteau)

    def _initialiser_persistance(self, fichier: Optional[Path],
                                 auto_calibration: bool,
                                 auto_persistance: bool):
        """Prépare la logique pour la calibration et la persistance automatique ou manuelle"""
        if fichier is None:
            self.persistance = None
            self.auto_persistance = False
            self.auto_calibration = False
        else:
            self.persistance = FuniPersistance(fichier=fichier)
            self.auto_persistance = auto_persistance
            self.auto_calibration = auto_calibration

    @staticmethod
    def _poteaux_liste_a_dict(poteaux: list[Poteau]) -> dict[str, Poteau]:
        """Crée un dict avec la liste de poteaux, en utilisant le nom comme clé"""
        poteaux_dict = {}
        for poteau in poteaux:
            poteaux_dict[poteau.nom] = poteau
        return poteaux_dict
