from sys import platform, executable
import pathlib
import os

python_exec = pathlib.Path(executable)
python_exec = f"{python_exec.stem}{python_exec.suffix}"

if not pathlib.Path(".venv").exists():
    os.system(f"{python_exec} -m pip install -U pip")
    os.system(f"{python_exec} -m venv .venv")

if platform == 'win32':
    python_venv_exec = str(pathlib.Path(f".venv/Scripts/{python_exec}"))
else:
    python_venv_exec = str(pathlib.Path(f".venv/bin/{python_exec}"))

os.system(f"{python_venv_exec} -m pip install -r requirements.txt")
