# Projet FuniBot - Néorobrooke
<img src="logo/NeoRobrooke.png" alt="Alt" width="100"/>

[![License](https://img.shields.io/github/license/Neorobrooke/neorobrooke-s4)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Tests Python](https://img.shields.io/github/workflow/status/Neorobrooke/neorobrooke-s4/Tests%20Python/main?label=Tests%20Python)](https://github.com/Neorobrooke/neorobrooke-s4/actions?query=workflow%3A%22Tests+Python%22)
[![Couverture Python](https://img.shields.io/codecov/c/gh/Neorobrooke/neorobrooke-s4/main?flag=python_api&label=Couverture%20Python)](https://codecov.io/gh/Neorobrooke/neorobrooke-s4/branch/main)

## Projet S4 en Génie robotique - Université de Sherbrooke

Le projet consiste à réaliser un montage et une librairie pour contrôler un robot suspendu par quatre câbles.
La librairie est principalement en langage Arduino.
Une API pour la librairie sera développée en Python.

## Vidéo promotionnelle
[![Vidéo promotionnelle](http://img.youtube.com/vi/ZmdO61vBWyo/0.jpg)](http://www.youtube.com/watch?v=ZmdO61vBWyo "Vidéo promotionnelle")

# git-lfs
Ce répertoir utilise git-lfs pour les fichiers volumineux.
Installez git-lfs avant de cloner.
## Linux
Disponible dans le gestionnaire de paquets de votre distribution.
## Windows ou autres
Téléchargeable à partir [de ce lien.](https://git-lfs.github.com/)

# Guide complet pour l'installation et l'assemblage du système
Un guide complet d'installation et d'assemblage du système est disponible [dans le répertoire "documentation".](https://github.com/Neorobrooke/neorobrooke-s4/blob/main/documentation/Manuel%20d'utilisation%20du%20Funibot.pdf)
Ce manuel décrit toutes les étapes pour assembler le système Funibot et mettre en place un environnement de développement pour utiliser la librairie avec le système.
Un guide de démarrage rapide pour mettre en place un environnement de développement logiciel seulement est disponible dans la section suivante de ce document.

# Initialisation logicielle rapide pour utiliser et/ou modifier la librarie
Il est possible d'initialiser un environnement Python contenant toutes les dépendances requises en exécutant le script `pip_script.py`.
Ce script crée un environnement virtuel et y installe les dépendances.
Il faut ensuite activer l'environnement à l'aide d'une commande dépendant du shell utilisé:

Windows (CMD) : `'./.venv/Scripts/activate.bat'`  
Windows (PowerShell) : `'./.venv/Scripts/Activate.ps1'`  
Windows (git-bash) : `source ./.venv/Scripts/activate`  
Linux/Mac (bash, zsh, etc.) : `source ./.venv/bin/activate`

L'environnement doit être réactivé chaque fois qu'on veut exécuter le module ou un autre module ou script qui en dépend.

## Méthode alternative pour utiliser la librairie sans la modifier
Il est possible d'installer la librairie directement avec `pip` si on ne souhaite pas la modifier, mais seulement l'utiliser.
1. Cloner le répertoire git de la librairie, et noter l'endroit où il se trouve.
2. Créer un dossier pour votre projet
3. Créer un environnement virtuel dans ce répertoire avec `python -m venv .venv`
4. Activer l'environnement virtuel avec l'une des commande `activate` mentionnées plus haut, selon votre système.
5. Mettez `pip` et `setuptools` à jour avec `python -m pip install -U pip setuptools`
5. Installer la librairie et ses dépendances avec `python -m pip install <chemin du root du git cloné>`
    - Vous pouvez installer des outils de test et/ou de développement (`pytest`,  `pytest-cov`, ainsi que `autopep8` et `ipython`) en faisant plutôt `python -m pip install <chemin du root du git cloné>[test,dev]`
      - Les outils de test aident à exécuter des tests unitaires (`pytest`) et à évaluer la couverture des tests (`pytest-cov`)
      - Les outils de développement permettent de formatter automatiquement vos fichiers python (`autopep8`), et offrent une console python interactive plus pratique que celle par défaut (`ipython`).

# Performance
## Précision
Testé avec un stabilisateur de 340 g à 275 mm (0.9163 N.m) et une zone de 1,2 m x 1,2 m.
Plus la nacelle s'approche d'un pôle, plus l'erreur est élevée.
- Position ± 25 mm
- Orientation ± 31°

## Limite
- Masse maximale testée (nacelle exclue): 1,2 kg
- Vitesse moyenne pour déplacement diagonal (nacelle + stabilisateur 340 g): 73 mm/s
