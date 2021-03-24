# Communication série entre le OpenCR et l'API

## Concepts généraux
La `commande` indique ce avec quoi on travaille, et le `type` indique si on veut ajouter/changer ou obtenir.
La réponse à `get` ou `set` est `ack` avec la valeur.

## Commandes JSON selon la librairie
### Initialisation
- Positionner les poteaux de soutien dans l'espace
  ```json
  {
    "comm": "pot",
    "type": "get | set | ack",
    "args": 
    {
      "id": "identifiant_du_poteau",
      "pos_x": 0.0,
      "pos_y": 0.0,
      "pos_z": 0.0
    }
  }
  // pos_x, pos_y et pos_z correspondent aux coordonnées du vecteur position du poteau additionné 
  ```
- Choisir un port série pour le système
  - Pas de comande
- Calibrer le système [À DÉTAILLER]
  - Calibration manuelle avec le mode `cable` et la longueur des câbles
  - Utilisation avec `get` et le mode `cable` pour obtenir la longueur des câbles
  - Utilisation avec `set` et le mode `sol` pour configurer la position du sol
    - Sert à définir la zone de travail à l'extérieure de laquelle le robot ne doit pas se rendre
    - `long` correspond à la position du sol en `y`, par rapport au référentiel global
    - `id` est ignoré, il peut être `null` ou complètement absent
  ```json
  {
    "comm": "cal",
    "type": "get | set | ack",
    "args":
    {
      "mode": "cable | sol",
      "id": 0,
      "long": 0.0
    }
  }
  ```

### Position et déplacement
- Obtenir la position de la charge dans l'espace
- Déplacer la charge à une position spécifiée
  ```json
  // Les positions sont `null` ou ignorées pour `get`.
  {
    "comm": "pos",
    "type": "get | set | ack",
    "args":
    {
      "pos_x": 0.0,
      "pos_y": 0.0,
      "pos_z": 0.0
    }
  }
  ```
- Déplacer la charge dans une direction spécifiée
  - Sur une certaine distance (ou l'atteinte de la limite)
  - Jusqu'à une demande d'arrêt (ou l'atteinte de la limite)
  ```json
  // `get` n'est pas utilisé. La norme du vecteur (axe_x, axe_y, axe_z) n'est pas considérée avec `distance`
  {
    "comm": "dep",
    "type": "set | ack",
    "args":
    {
      "mode": "start | stop | distance",
      "axe_x": 0.0,
      "axe_y": 0.0,
      "axe_z": 0.0
    }
  }
  ```

### Erreurs et exceptions
- Accéder aux erreurs levées
- Obtenir le dernier message d'erreur
- Effacer les erreurs et réinitialiser
  ```json
  // Avec `get`, `args` lui-même est `null`
  // `code` est le code d'erreur (un entier)
  // `maj` contient `true` si l'erreur est majeure, `false` sinon
  // `t` contient une identification du moment de l'erreur
  // `num` contient le nombre d'erreurs restantes
  {
    "comm": "err",
    "type": "get | ack",
    "args":
    {
      "id": 0,
      "maj": false,
      "t": 0,
      "err_sup": 1
    }
  }
  ```

