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
      "id": 0,
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

### Contrôle des moteurs
- Activer, désactiver ou réinitialiser les moteurs
  - `get` permet de voir si les moteurs sont actifs ou pas
    - S'utilise avec `mode` qui est `null`
    - La réponse est mise dans le `mode`, à `on` ou `off`
  - `set` permet de mettre les moteurs à `on` ou à `off`, ou de les réinitialiser avec `reset`
  ```json
  {
    "comm": "mot",
    "type": "get | set | ack",
    "args":
    {
      "mode": "on | off | reset"
    }
  }
  ```

### Synchronisation
- Obtenir la tâche actuelle du système
  - Les tâches sont les suivantes:
    - `arr` lorsque le système est à l'arrêt
    - `dir` lorsque le système est en déplacement directionnel sans condition d'arrêt
    - `pos` lorsque le système est en déplacement vers une position spéficique ou dans une direction mais d'une certaine longueur
  ```json
  {
    "comm": "reg",
    "type": "get | ack",
    "args":
    {
      "tache": "arr | dir | pos"
    }

  }
  ```
- Obtenir un estimé de la durée minimale avant la fin de la tâche en cours
  - Les tâches sont les suivantes:
    - `arr` lorsque le système est à l'arrêt
    - `dir` lorsque le système est en déplacement directionnel
    - `pos` lorsque le système est en déplacement vers une position
  - La durée retournée dans `tmp` est en secondes
    - `tmp` est utilisé par `ack` seulement pour répondre, et est à `null` avec `get`
  ```json
  {
    "comm": "dur",
    "type": "get | ack",
    "args":
    {
      "tmp": 0.0
    }
  }
  ```
- Attendre la fin de la tâche en cours
  - Premier échange
    - Premier appel avec `set`
      - `fin` est `false`, on est au premier appel
      - `val` est `null`
    - Première réponse avec `ack`
      - `fin` est `false`, on est à la première réponse
      - `val` peut avoir deux valeurs
        - `true` si le robot bouge et que d'attendre est valide
        - `false` si le robot ne bouge pas et que d'attendre n'est pas valide
    - Si `val` est `true`, on passe au second échange
  
  - Second échange
    - Second appel avec `set`
      - `fin` est `true`, on est à l'appel attendant la fin
      - `val` est `null`
      - On reste bloqué en attendant la réponse, qui ne viendra que lorsque le déplacement sera fini
    - Le déplacement se poursuit, puis se termine
    - Seconde réponse avec `ack`
      - `fin` est `true`, on a fini de bouger
      - `val` peut avoir deux valeurs:
        - `true` si la fin est causée par l'atteinte de la position
        - `false` si la fin est causée par une erreur ou par l'atteinte des limites de la zone de travail
  ```json
  {
    "comm": "att",
    "type": "set | ack",
    "args":
    {
      "val": true,
      "fin": false
    }
  }
  ```

### Erreurs et exceptions
- Commande d'erreurs
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
      "err_sup": 0
    }
  }
  ```
- Commande de log
  - Afficher les messages de déboguage
  - Avec `get`, reçoit le *buffer* au complet
  - Avec `ack`, envoit le *buffer* au complet
  ```json
  {
    "comm": "log",
    "type": "get | ack",
    "args":
    {
      "msg": "message de déboguage quelconque\nContient plusieurs messages",
    }
  }
  ```
