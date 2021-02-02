# Commandes de l'application de tests en CLI
## Initialisation
- Paramètre "-N" pour une liste de noeuds et leurs coordonnées
  - Paramètre de la forme suivante: "x1:y1 x2:y2 x3:y3 x4:y4"
- Paramètre "-p" pour le numéro du port série à utiliser

## Menu principal
- Commande "exit" ou "quitter" pour quitter
- Commande "cal" ou "calibrer" pour calibrer
- Commande "ls" ou "liste" pour afficher la position des pôles et la longueur des câbles
- Commande "ll" ou "liste-tout" pour afficher, pour chaque pôle:
  - Les coordonnées du pôle
  - La longueur du câble
  - Le couple du moteur [À VALIDER]
  - Le courant dans le moteur [À VALIDER]
  - Autre informations pertinentes [À AJOUTER]
- Commande "pos" ou "position" pour afficher la position de la charge
- Commande "dep" ou "deplacer" pour contrôler le robot avec les flèches du clavier
- Commande "go" ou "aller" pour déplacer le robot à une position spécifique

## Autres actions
 - Ctrl-C pour annuler un déplacement en cours
 - Ctrl-C pour quitter si on est au menu principal
 - Flèches pour déplacer en mode 'dep'
 - WASD pour déplacer en mode 'dep'
 - HJKL pour déplacer en mode 'dep'