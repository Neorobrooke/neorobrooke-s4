from sys import platform, executable
import pathlib
import os

if platform == 'win32':
    python_exec = executable.split('\\\\')[-1]
else:
    python_exec = executable.split('/')[-1]

if not pathlib.Path(".venv").exists():
    os.system(f"{python_exec} -m pip install -U pip")
    os.system(f"{python_exec} -m venv .venv")

if platform == 'win32':
    python_venv_exec = str(pathlib.Path(".venv/Scripts/python.exe"))
else:
    python_venv_exec = str(pathlib.Path(".venv/bin/python"))

os.system(f"{python_venv_exec} -m pip install -r requirements.txt")
