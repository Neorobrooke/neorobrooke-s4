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
  ```
- Choisir un port série pour le système
  - Pas de comande
- Calibrer le système [À DÉTAILLER]
  ```json
  {
    "comm": "cal",
    "args": "à définir"
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
  // `flag` est vrai si l'erreur est levée
  // `msg` contient une string si l'erreur est levée
  // si `code` est `null`:
  //    Avec get, donne une réponse pour chaque code d'erreur dont le flag est vrai. Le `num` de chaque réponse est le nombre total de réponses + 2 (ack vides au début et à la fin)
  //    Avec set, efface toutes les erreurs en réinitialisant tout ce qu'il faut, et répond pour chaque erreur qui avait un `flag` vrai. Le `num` de chaque réponse est le nombre total de réponses + 2 (ack vides au début et à la fin)
  //    Avec ack, `code` est null au début et à la fin des réponses multiples
  {
    "comm": "err",
    "type": "get | set | ack",
    "args":
    {
      "code": "un identifiant d'erreur",
      "flag": false,
      "msg": null,
      "num": 1
    }
  }
  ```

