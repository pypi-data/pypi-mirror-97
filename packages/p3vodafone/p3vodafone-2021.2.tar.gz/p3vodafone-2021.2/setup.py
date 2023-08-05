#!/usr/bin/env python3
import pathlib

from setuptools import setup
try:
    import py2exe
except NameError:
    print("PY2EXE Could not be loaded")

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="cp1250")

setup(
    name="p3vodafone",
    description="",
    packages=[
        "p3vodafone",
    ],
    package_data={
        "": ["*.ttf"],
    },
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/otevrenamesta/praha3/vyuctovani-vodafone",
    author="Štěpán Štrébl",
    author_email="strebl.stepan@praha3.cz",
    license="AGPL-3.0",
    version="2021.2",
    install_requires=[
        'pandas~=1.2.1',
        'reportlab~=3.5.59',
        'openpyxl~=3.0.6',
        'pytk',
        'profig',
        'appdirs',
        'packaging',
    ],
    options={
        "py2exe": {
            "includes": [
                "reportlab",
                "pandas",
                "numpy",
                "setuptools",
                "xml.etree",
                "reportlab.rl_settings",
                "p3vodafone",
                "openpyxl",
                "packaging",
                "packaging.specifiers",
                "packaging.requirements",
            ],
        }
    },
    entry_points={
        'console_scripts': [
            'vyuctovani-vodafone=p3vodafone.user_interface:gui'
        ]
    }
)
