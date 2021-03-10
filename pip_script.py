from sys import platform
import pathlib
import os


if not pathlib.Path(".venv").exists():
    os.system("py -m pip install -U pip")
    os.system("py -m venv .venv")

if platform == 'win32':
    os.system("\"%cd%/.venv/Scripts/activate.bat\" && py -m pip install -r requirements.txt")
else:
    os.system("source .venv/Scripts/activate && py -m pip install -r requirements.txt")
