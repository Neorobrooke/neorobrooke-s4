# API Python

## Module `funibot`

### Classe `Funibot`
- Représente un Funibot.
- Lié à un port série accessible via l'attribut `port_serie`
- Offre l'accès aux différents poteaux
  - Itération
  - Accès par crochets: [id_poteau]
  - Accès au `dict` par l'attribut `poteaux`
- Offre l'accès à la position actuelle de la charge
  - Attribut: `pos`
- Permet de déplacer la charge à une position donnée
  - Attribut: `pos = Vecteur(x=1, y=1, z=1)`
- Permet de déplacer la charge dans une direction donnée, d'une certaine distance
  - Méthode: `deplacer(direction: Union[Direction, Vecteur, str], distance=None)`
  - Avec une str:
    - Direction créée à partir de la str
- Permet de déplacer la charge dans une direction donnée, jusqu'à ce qu'on l'arrête
  - Context Manager:
    ```py
    with deplacer(direction: Union[Direction, Vecteur, str]):
        # faire_des_trucs_pendant_que_ca_bouge()
        pass
    ```
  - Interrompu par un Ctrl-C

### Classe `Direction`
 - Créé avec 1 à 3 axes, avec + (implicite) ou - pour chacun, peu importe l'ordre
 - Exemple: `Direction("+x+y-z")`
 - Exemple: `Direction("-z-x+y")`
 - Exemple: `Direction("x")`
 - Peut être transformé en vecteur PosVec avec la méthode `vecteur`

### Classe `Vecteur`
- Contient trois composantes/coordonnées x, y et z
- Algèbre simple possible (somme, différence, multiplication par un nombre, division par un nombre, divison entière par un nombre)
- Obtention de la norme avec la méthode `norme`
- Obtention du vecteur unitaire avec la méthode `unitaire`

### Classe `Poteau`
- Réprente un poteau supportant un des pôles du Funibot.
- Accessible via un Funibot:
  - Itération, [ ], attribut `poteaux`
- Donne accès à la position du pôle:
  - Attribut `pos`
- Donne accès à la longueur du câble à ce pôle
  - ~~Fonction `len()`~~
  - Attribut `longueur_cable`
- Donne accès au courant dans le moteur (et au couple?)
  - Attributs `courant_moteur` (et `couple_moteur`?)

## Module `json_serial`

### Classe `Serial`
- Contient une communication série sur un certain port série
- Permet l'envoi et la réception de messages JSON
- Ne contient rien en lien avec le Funibot.

## Module `funibot_json_serial`

### Classe `FunibotSerial`
- Dérive de `json_serial.Serial`
- Offre des accès faciles pour envoyer ou recevoir les commandes du Funibot