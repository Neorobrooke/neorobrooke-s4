from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf8')

setup(
    name="funibot-neorobrooke",
    version="2.0.0-alpha",
    author="Néorobrooke",
    author_email="warp0901@usherbrooke.ca",
    description="Permet de contrôler un Funibot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    url="https://github.com/Neorobrooke/neorobrooke-s4",
    classifiers=[
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8"
        "Programming Language :: Python :: 3.9"
        "License :: OSI Approved :: BSD License"
        "Operating System :: OS Independent"
        "Natural Language :: French"
    ],
    package_dir={'': 'Code/API'},
    packages=find_packages(include="*api"),
    test_suite = "tests",
    py_modules=["funibot_cli"],
    python_requires=">=3.7, <3.10",
    install_requires=[
        "PyYAML >= 5.4.1",
        "ruamel.yaml >= 0.17.2",
        "pyserial >= 3.5",
        "python-benedict >= 0.23.2"
    ],
    package_data={
        'funibot_api': ["../config.yaml", "../../positionnement/dictionnaireErreur.txt"],
    },
    # data_files=[('funibot_config', ['Code/API/config.yaml'])],
    extras_require={
        "dev": ["autopep8 >= 1.5.6", "ipython >= 7.22.0"],
        "test": ["pytest >= 6.2.2", "pytest-cov >= 2.11.1"]
    },
    entry_points={
        "console_scripts": [
            "funibot_cli=funibot_cli:main",
        ],
    },
)