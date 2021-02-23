# Projet FuniBot - Néorobrooke
<img src="logo/NeoRobrooke.png" alt="Alt" width="100"/>

[![License](https://img.shields.io/github/license/Neorobrooke/neorobrooke-s4)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Tests Python](https://img.shields.io/github/workflow/status/Neorobrooke/neorobrooke-s4/Tests%20Python/main?label=Tests%20Python)](https://github.com/Neorobrooke/neorobrooke-s4/actions?query=workflow%3A%22Tests+Python%22)
[![Couverture Python](https://img.shields.io/codecov/c/gh/Neorobrooke/neorobrooke-s4/main?flag=python_api&label=Couverture%20Python)](https://codecov.io/gh/Neorobrooke/neorobrooke-s4/branch/main)
[![Tests C++](https://img.shields.io/github/workflow/status/Neorobrooke/neorobrooke-s4/Tests%20C++/main?label=Tests%20C%2B%2B)](https://github.com/Neorobrooke/neorobrooke-s4/actions?query=workflow%3A%22Tests+C%2B%2B%22)

## Projet S4 en Génie robotique - Université de Sherbrooke

Le projet consiste à réaliser un montage et une librairie pour contrôler un robot suspendu par quatre câbles.
La librairie est principalement en langage Arduino.
Une API pour la librairie sera développée en Python.

# git-lfs
Ce répertoir utilise git-lfs pour les fichiers volumineux.
Installez git-lfs avant de cloner.
## Linux
Disponible dans le gestionnaire de paquets de votre distribution.
## Windows ou autres
Téléchargeable à partir [de ce lien.](https://git-lfs.github.com/)

# Initialisation
Il est possible d'initialiser un environnement Python contenant toutes les dépendances requises en exécutant le script `pip_script.py`.
Ce script crée un environnement virtuel et y installe les dépendances.
Il faut ensuite activer l'environnement à l'aide d'une commande dépendant du shell utilisé:

Windows (CMD) : `'./.venv/Scripts/activate.bat'`  
Windows (PowerShell) : `'./.venv/Scripts/Activate.ps1'` 
Windows (git-bash) : `source ./.venv/Scripts/activate`
Linux/Mac (bash, zsh, etc.) : `source ./.venv/bin/activate`

L'environnement doit être réactivé chaque fois qu'on veut exécuter le module ou un autre module ou script qui en dépend.
