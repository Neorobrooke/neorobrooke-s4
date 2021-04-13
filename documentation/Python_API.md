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
  - Méthode: `deplacer(direction: Union[Direction, Vecteur, str], distance: float = None)`
  - Avec une str:
    - Direction créée à partir de la str
  - Si `distance == None`
    - Arrêt avec la méthode `stop`
      - Annule aussi tout déplacement en cours, dont un déplacement résultant d'une assignation à `pos`
  - Si `distance == 0`
    - La norme du vecteur `direction` est utilisé comme distance du déplacement
  - Si `distance == L`
    - Le vecteur `direction` ne sert que pour la direction, et le déplacement est d'une distance `L`
  - Retourne une liste des erreurs `FuniErreur`
- Offre l'accès à la position du sol avec l'attribut `sol`
  - Une assignation à `sol` permet de modifier la position du sol
  - La position du sol est le plan horizontal le plus bas auquel le robot peut se rendre
- Permet de connaître l'état du Funibot
  1. Arrêté si `en_deplacement() is False`, si `arrete() is True` ou si `regime() == eFuniRegime.ARRET`
  2. En déplacement directionnel si `en_deplacement() is True`, si `arrete() is False` ou si `regime() == eFuniRegime.DIRECTION`
    - Défini comme un déplacement sans condition de fin
    - Ne s'arrêtera que lorsqu'on fera `stop()`
  3. En déplacement positionnel si `en_deplacement() is True`, si `arrete() is False` ou si `regime() == eFuniRegime.POSITION`
    - Défini comme un déplacement avec une condition de fin (distance ou position)
    - S'arrêtera de lui-même
- Permet d'avoir une durée estimée du déplacement en cours
  - Avec l'attribut `duree_estimee`
  - Ne donne une valeur que pour un déplacement avec une condition de fin (distance ou position)
- Possibilité d'attendre la fin du déplacement en cours
  - La méthode `attendre` bloque jusqu'à ce que le déplacement en cours soit terminé
  - Si le robot ne bouge pas ou se déplace sans condition de fin (distance ou déplacement), la commande retourne immédiatement avec une valeur de retour indiquant que l'attente n'était pas possible
  - La méthode `tout_attendre` s'utilise comme un `Context Manager`
    ```py
    with bot.tout_attendre() as liste_retours:
        bot.pos = Vecteur()
        print(bot.pos)
        bot.deplacer(Vecteur(1,2,0))
    
    print(liste_retours[-1].retour_attendre)
    ```
    - Tous les déplacements (en assignant à `pos` ou par la méthode `deplacer`) seront automatiquement suivis par une attente implicite.
    - Les résultats de chacune de ces attentes seront ajoutés à la liste retournée par le `Context Manager` (dans l'exemple, `liste_retours`)
    - Chaque élément de la liste est une structure contenant deux membres
      1. `retour_attendre`, la valeur du retour de l'attente
      2. `nom_methode`, qui est le nom de la méthode pour laquelle l'attente a été appliquée
- Possibilité de gérer l'état des moteurs
  - Connaître l'état avec l'attribut `moteurs_actifs`
  - Activer ou désactiver les moteurs en assignant un `bool` à l'attribut `moteurs_actifs`
  - Réinitialiser les moteurs avec la méthode `reinitialiser_moteurs`
- Accès aux erreurs du Funibot sur le OpenCR sous forme de `list` avec la méthode `erreur`
- Accès au log de déboguage du OpenCR avec la méthode `log`
  - Retourne une longue `str` sur plusieurs lignes correspondant au log complet depuis la dernière demande du log

## Module `funilib`

### Classe `Vecteur`
- Contient trois composantes/coordonnées x, y et z
- Algèbre simple possible (somme, différence, multiplication par un nombre, division par un nombre, divison entière par un nombre, comparaison d'égalité)
- Obtention de la norme avec l'attribut `norme`
  - Changement de la norme en conservant la direction en assignant à `norme`
- Obtention du vecteur unitaire avec la méthode `unitaire`
- Obtention d'un `tuple` contenant les coordonnées `(x, y, z)` avec la méthode `vers_tuple`

### Classe `Direction`
- Créé à partir d'une chaîne de caractères
- Prend 1 à 3 axes, avec + (implicite) ou - pour chacun, peu importe l'ordre, et pouvant être précédé d'une valeur (1 implicite)
  - Exemple: `Direction("+x+y-z")`
  - Exemple: `Direction("-35.76z-x43+2y")`
  - Exemple: `Direction("x")`
  - Exemple: `Direction("4,5x")`
- Les valeurs réelles peuvent être écrites avec un point `.` ou une virgule `,`
- Peut être transformé en Vecteur avec la méthode `vecteur`

### Classe `Poteau`
- Réprente un poteau supportant un des pôles du Funibot.
- Accessible via un Funibot:
  - Itération
  - [] et attribut `poteaux` (`dict`, accessible par le nom)
  - Attribut `poteaux_id` (`list`, accessible par l'id selon le OpenCR)
- Donne accès à la position du pôle:
  - Attribut `pos_pole`
- Donne accès à la position de l'accroche:
  - Attribut `pos_accroche`
- Donne accès à la longueur du câble à ce pôle
  - Attribut `longueur_cable`
  - Assigner à l'attribut `longueur_cable` permet une calibration manuelle par longueur initiale des câbles
- Attributs `nom` et `id`
  - `nom` est donnée à la création
  - `id` est donné lorsque le poteau est initialisé auprès du OpenCR

## Module `funiserial`

### Classe `FunibotSerial`
- Offre une abstraction pour envoyer ou recevoir les commandes séries entre le Funibot et l'API

## Module `funiconfig`

### Classe `FuniConfig`
- Permet de configurer un Funibot
- Peut être rempli à la main (attribut par attribut) ou généré à partir d'un fichier de configuration et de quelques valeurs supplémentaires

### Classe `FuniArgs`
- Permet de fournir des arguments CLI par défaut au Funibot (`argparse`)
- Peut être étendu avec d'autres arguments CLI en passant en un `argparse.ArgParser` déjà partiellement configuré en argument à la construction
- Permet de générer automatiquement un FuniConfig à partir des arguments CLI 
  - L'un de ces arguments est le chemin du fichier de configuration

## Module `funipersistance`

### Classe `FuniPersistance`
- Gère le fichier de persistance
- Permet de conserver la calibration du Funibot entre ses redémarrages

## Module `funimock`
- Utilisé pour réaliser des tests automatisés, ou pour tester manuellement sans accès au matériel

### Interface `IMockSerial`
- Interface contenant les méthodes et de la classe `serial.Serial` utilisés par le Fnuibot
- Sert de base aux classes `MockSerial` et `DualMockSerial`

### Classe `MockSerial`
- Représente une fausse communication série en boucle fermée
- La réponse à chacun des messages du Funibot est l'exact même message, mais avec le `type` changé de `get` ou `set` à `ack`

### Classe `DualMockSerial`
- Contient un `MockSerial` pour la lecture et un `MockSerial` en écriture
- Il est possible d'imposer des réponses aux prochains messages du `Funibot`
- Utilisé pour des tests automatisés plus complexes nécessitant d'interpréter correctement les réponses du OpenCR
