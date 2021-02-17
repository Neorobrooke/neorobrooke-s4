from sys import platform
import pathlib
import os


if not pathlib.Path(".venv").exists():
    os.system("python -m pip install -U pip")
    os.system("python -m venv .venv")

if platform == 'win32':
    os.system("\"%cd%/.venv/Scripts/activate.bat\" && python -m pip install -r requirements.txt")
else:
    os.system("source .venv/Scripts/activate && python -m pip install -r requirements.txt")
