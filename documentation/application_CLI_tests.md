# Commandes de l'application de tests en CLI

## Initialisation
- Paramètre "-f" pour le fichier de config à utiliser
  - Format YAML
  - Exemple pour deux poteaux nommés `moteur1` et `moteur4`
  ```yaml
  ---
  serial:
    port: COM5
    baudrate: 57600
  poteaux: # distances en mm
    moteur1:
      poles:
        x: 0
        y: 0
        z: 0
      accroches:
        x: -55
        y: 100
        z: 0
    moteur4:
      poles:
        x: 1180
        y: 0
        z: 0
      accroches:
        x: 55
        y: 100
        z: 0
  ...
  ```
  - `poles` est un vecteur position indiquant le dernier contact entre le poteau et le câble
  - `accroche` est un vecteur indiquant la position de l'attache du câble sur la nacelle, par rapport au TCP (Tool Center Point, le point qu'on cherche à positionner dans l'espace)
  - Tous les vecteurs doivent être dans la même base vectorielles
    - La base doit respecter la règle de la main droite
  - L'axe `y` doit être dans le sens opposé à la gravité
    - Il doit donc être vertical orienté vers le haut
- Paramètre `--mock` pour mocker le port série

## Menu principal
- Commande `exit` pour quitter
- Commande `clear` pour effacer le terminal
- Commande `shell` pour exécuter une commande dans le shell sous-jacent
  - Utilisable aussi en précédant la commande externe d'un `!`
- Commande `help` pour avoir de l'information sur une commande
  - Utilisable aussi en précédant le nom d'une commande d'un `?`
- Commande `stop` pour arrêter tout mouvement du robot
- Commande `cal` pour calibrer automatiquement `[PAS IMPLÉMENTÉ]`
- Commande `ls` pour afficher la position des pôles et la longueur des câbles
  - `[PARTIELLEMENT IMPLÉMENTÉ]` Ne donne que la position des pôles et des attaches, pas la longueur des câbles
  - Peut être utilisé avec un argument pour ne donner les informations que sur un poteau
    - L'argument peut être le nom du poteau ou son ID selon le OpenCR (un entier)
      - Pour utiliser l'ID selon le OpenCR, ajouter un `:` devant
      - Exemple: `ls 1` liste le poteau dont le nom est `1` dans le fichier de config
      - Exemple: `ls :1` liste le poteau dont l'ID est `1` selon le OpenCR
- Commande `pos` pour afficher la position de la charge
- Commande `dep` pour déplacer le robot dans une direction simple donnée
  - Pour arrêter le robot, utiliser la commande `stop`
  - Format:
    - Une châine contenant les caractères `+`, `-`, `x`, `y`, et `z`
    - x, y, et z sont les mêmes axes que les vecteurs du fichier de config
    - Une lettre présente sans signe `+` ou `-` en avant est considérée comme `+`
    - Une lettre absente est considérée comme 0 (pas de déplacement dans cet axe)
  - Exemples:
    - `dep xy` -> Déplacement selon le vecteur `(1;1;0)`
    - `dep -yz` -> Déplacement selon le vecteur `(0;-1;1)`
    - `dep -xy-z` -> Déplacement selon le vecteur `(-1;1;-1)`
    - `dep -z` -> Déplacement selon le vecteur `(0;0;-1)`
- Commande `cable` pour calibrer manuellement selon la longueur des câbles
  - Requis une seule fois au lancement ou reset de l'OpenCR
  - Peut être faite en tout temps pour recalibrer le robot
  - Format:
    - `cable nom_poteau_1:longueur_1 [nom_poteau_2:longueur_2 ...]`
    - Un ou plusieurs câbles peuvent être calibrés en une commande
  - `longueur_i` doit être un nombre réel
  - `nom_poteau_i` doit correspondre à un nom de poteau existant dans le fichier de configuration
- Commande `go` pour déplacer le robot à une position spécifique
  - Format: `go x:y:z`, avec `x`, `y` et `z` comme des nombres formant un vecteur position, en millimètres
- Commande `serial` pour envoyer manuellement une commande JSON au robot et afficher sa réponse.
  - Voir le document [sur la documentation série ici.](./communication_serie.md)
- Commande `err` pour demander et afficher toutes les erreurs générées par le OpenCR, avec un timestamp.
  - Voir le [dictionnaire des erreurs ici.](../Code/positionnement/dictionnaireErreur.txt)

## Autres actions
 - Ctrl-C pour annuler un déplacement en cours `[PAS IMPLÉMENTÉ]`
 - Ctrl-C pour quitter si on est au menu principal