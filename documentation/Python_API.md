# API Python

## Module `funibot`

### Classe `Funibot`
- Représente un Funibot.
- Lié à un port série accessible via l'attribut `port_serie`
- Offre l'accès aux différents poteaux
  - Itération
  - Accès par crochets: [nom_poteau]
  - Accès au `dict` par l'attribut `poteaux`
  - Accès par l'id donné par l'OpenCR via l'attribut `poteaux_id` (une `list`)
- Offre l'accès à la position actuelle de la charge
  - Attribut: `pos`
- Permet de déplacer la charge à une position donnée
  - Attribut: `pos = Vecteur(x=1, y=1, z=1)`
- Permet de déplacer la charge dans une direction donnée, d'une certaine distance ou jusqu'à ce qu'on l'arrête
  - Méthode: `deplacer(direction: Union[Direction, Vecteur, str], distance=None)`
  - `[À VENIR]` Déplacement d'une certaine distance
  - Avec une str:
    - Direction créée à partir de la str
    - Vecteur créé à partir de la str `[À VENIR]`
  - Arrêt avec la méthode `stop`
    - Annule aussi un déplacement avec toute autre manière, dont une assignation à `pos`

### Classe `Direction`
 - Créé avec 1 à 3 axes, avec + (implicite) ou - pour chacun, peu importe l'ordre
 - Exemple: `Direction("+x+y-z")`
 - Exemple: `Direction("-z-x+y")`
 - Exemple: `Direction("x")`
 - Peut être transformé en vecteur PosVec avec la méthode `vecteur`

### Classe `Vecteur`
- Contient trois composantes/coordonnées x, y et z
- Algèbre simple possible (somme, différence, multiplication par un nombre, division par un nombre, divison entière par un nombre)
- Obtention de la norme avec l'attribut `norme`
  - Changement de la norme en conservant la direction en assignant à `norme`
- Obtention du vecteur unitaire avec la méthode `unitaire`

### Classe `Poteau`
- Réprente un poteau supportant un des pôles du Funibot.
- Accessible via un Funibot:
  - Itération, [ ], attribut `poteaux`
- Donne accès à la position du pôle:
  - Attribut `pos`
- Donne accès à la longueur du câble à ce pôle
  - Attribut `longueur_cable`
  - Assigner à l'attribut `longueur_cable` permet une calibration manuelle par longueur initiale des câbles
- Donne accès au courant dans le moteur (et au couple?) `[PAS IMPLÉMENTÉ]`
  - Attributs `courant_moteur` (et `couple_moteur`?)

## Module `funibot_json_serial`

### Classe `FunibotSerial`
- Offre des accès faciles pour envoyer ou recevoir les commandes du Funibot