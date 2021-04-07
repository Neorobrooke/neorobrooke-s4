# Commandes de l'application de tests en CLI

## Initialisation
- Paramètre `-f` pour le fichier de configuration à utiliser
  - Format YAML
  - Paramètres pour le port série
    - Le port peut être supplanté par un paramètre en ligne de commande, `--port`
  - Position du sol (en mm)
    - Utilisée pour la gestion de la zone de travail
  - Paramètres de persistance
    - `fichier` est le chemin du fichier à utiliser pour la persistance
      - Peut être supplanté par un paramètre en ligne de commande, `-c`
    - `auto-persistance` détermine si on enregistre automatiquement la calibration lors de la fermeture du programme
    - `auto-calibration` détermine si on charge automatiquement la calibration lors de l'ouverture du programme
    - `auto-persistance` et `auto-calibration` peuvent être forcés par des paramètre en ligne de commande, `--auto-persistance` et `--auto-persistance`
  - Exemple pour quatre poteaux nommés `pot0` à `pot3`
  ```yaml
  ---
  serial:
    port: COM5
    baudrate: 57600
  sol: -800
  persistance:
    fichier: Code/API/calibration.yaml
    auto-persistance: False
    auto-calibration: False
  poteaux: # distances en mm
    - pot0:
        poles:
          x: 0
          y: 0
          z: 0
        accroches:
          x: -60
          y: 100
          z: -60
    - pot1:
        poles:
          x: 1220
          y: 0
          z: 0
        accroches:
          x: 60
          y: 100
          z: -60
    - pot2:
        poles:
          x: 1220
          y: 0
          z: 1220
        accroches:
          x: 60
          y: 100
          z: 60
    - pot3:
        poles:
          x: 0
          y: 0
          z: 1220
        accroches:
          x: -60
          y: 100
          z: 60
  ...
  ```
  - `poles` est un vecteur position indiquant le dernier contact entre le poteau et le câble
  - `accroche` est un vecteur indiquant la position de l'attache du câble sur la nacelle, par rapport au TCP (Tool Center Point, le point qu'on cherche à positionner dans l'espace)
  - Tous les vecteurs doivent être dans la même base vectorielles
    - La base doit respecter la règle de la main droite
  - L'axe `y` doit être dans le sens opposé à la gravité
    - Il doit donc être vertical orienté vers le haut
  - Les distances sont en millimètres
- Paramètre `--mock` pour mocker le port série
  - Permet de tests sans le matériel
  - Certains comportements peuvent être indéfinis

## Menu principal
- Commande `exit` pour quitter
- Commande `clear` pour effacer le terminal
- Commande `shell` pour exécuter une commande dans le shell sous-jacent
  - Utilisable aussi en précédant la commande externe d'un `!`
- Commande `help` pour avoir de l'information sur une commande
  - Utilisable aussi en précédant le nom d'une commande d'un `?`
- Commande `stop` pour arrêter tout mouvement du robot
- Commande `cal` pour calibrer automatiquement à partir du fichier de persistance
- Commande `persi` pour enregistrer les longueurs des câbles actuelles dans le fichier de persistance
- Commande `ls` pour afficher la position des pôles
  - Peut être utilisé avec un argument pour ne donner les informations que sur un poteau
    - L'argument peut être le nom du poteau ou son ID selon le OpenCR (un entier)
      - Pour utiliser l'ID selon le OpenCR, ajouter un `:` devant
      - Exemple: `ls 1` liste le poteau dont le nom est `1` dans le fichier de config
      - Exemple: `ls :1` liste le poteau dont l'ID est `1` selon le OpenCR
- Commande `len` pour afficher la longueur des câbles
  - Même format que la commande `ls` ci-dessus.
- Commande `pos` pour afficher la position de la charge
- Commande `dep` pour déplacer le robot dans une direction simple donnée
  - Pour arrêter le robot, utiliser la commande `stop`
  - Format:
    - Une châine contenant les caractères `+`, `-`, `x`, `y`, et `z`
    - x, y, et z sont les mêmes axes que les vecteurs du fichier de config
    - Une lettre présente sans signe `+` ou `-` en avant est considérée comme `+`
    - Une lettre absente est considérée comme 0 (pas de déplacement dans cet axe)
    - Un nombre peut précéder chaque lettre mais suivre chaque signe
      - Peut être un entier ou un nombre décimal
      - Les nombres décimaux acceptent la virgule ou le point comme séparateur
      - Les nombres sont en millimètres
  - Exemples:
    - `dep 2x-47.34y` -> Déplacement selon le vecteur `(2;-47.34;0)`
    - `dep -yz` -> Déplacement selon le vecteur `(0;-1;1)`
    - `dep -xy-34z` -> Déplacement selon le vecteur `(-1;1;-34)`
    - `dep -3,1z` -> Déplacement selon le vecteur `(0;0;-3.1)`
- Commande `depv` pour déplacer le robot dans une direction, d'une distance correspondant à la norme du vecteur direction
  - Même syntaxe que la commande `dep` 
- Commande `depl` pour déplacer le robot dans une direction, d'une distance spécifiée
  - Même syntaxe que la commande `dep`
  - La distance doit être spécifiée en ajouant ` :N` à la fin, où `N` est un nombre réel positif, en millimètres
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
- Commande `sol` pour afficher la position du sol
  - Sert pour la limite de la zone de travail
- Commande ``chsol` pour modifier la position du sol
  - Sert pour la limite de la zone de travail
- Commande `mot` pour activer, désactiver ou réinitialiser les moteurs
  - Utiliser `mot on` pour activer les moteurs
    - `on` peut aussi être remplacé par `ON`, `1`, `true`, `TRUE`, `True`, `e` (pour "enable") ou `a` (pour "actif" ou "activer")
  - Utiliser `mot off` pour désactiver les moteurs
    - `off` peut aussi être remplacé par `OFF`, `0`, `false`, `FALSE`, `False`, `d` (pour "disable" ou "désactiver") ou `a` (pour "activer")
  - Utiliser `mot reset` pour réinitialiser les moteurs
    - `reset` peut aussi être remplacé par `reinit` ou `r`
- Commande `reg` pour afficher le régime actuel du Funibot
  - Affiche `ARRET` si le robot ne bouge pas
  - Affiche `DIRECTION` si le robot se déplace, mais n'arrêtera pas si une commande `stop` ne lui est pas envoyée
  - Affiche `POSITION` si le robot se déplace jusqu'à une position connue d'avance
- Commande `dur` pour afficher la durée estimée du déplacement en cours, en secondes
  - Affiche `0` si le régime n'est pas `POSITION`
- Commande `att` pour bloquer et attendre la fin du déplacement en cours
  - Affiche le résultat de l'attente
    - Terminée
    - Pas besoin d'attendre (le régime n'est pas `POSITION`)
      - Retourne immédiatement
    - Arrêt causé par une erreur ou l'atteinte des limites de la zone de travail
    - Erreur de communication empêchant de connaître le résultat de l'attente
- Commande `serial` pour envoyer manuellement une commande JSON au robot et afficher sa réponse.
  - Voir le document [sur la documentation série ici.](./communication_serie.md)
- Commande `err` pour demander et afficher toutes les erreurs générées par le OpenCR, avec un timestamp.
  - Voir le [dictionnaire des erreurs ici.](../Code/positionnement/dictionnaireErreur.txt)
- Commande `log` pour afficher le log du OpenCR
  - Utilisée pour le déboguage du OpenCR

## Autres actions
 - Ctrl-C pour annuler un déplacement en cours `[PAS IMPLÉMENTÉ]`
 - Ctrl-C pour quitter si on est au menu principal