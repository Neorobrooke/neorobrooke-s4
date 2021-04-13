from setuptools import setup
from glob import glob
from pathlib import Path

doc = [x for x in glob("documentation/*") if Path(x).is_file()]

setup(
    data_files = [
        ("share/funibot-neorobrooke", ["Code/API/config.yaml", "Code/API/calibration.yaml"]),
        ("share/funibot-neorobrooke/documentation", doc)
    ]
)
