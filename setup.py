"""Setup script for QuteStyle library."""

import importlib.metadata

from setuptools import setup

VERSION = importlib.metadata.version("qute_style")

setup(
    name="qute_style",
    version=VERSION,
    description="An expandable application framework for Qt",
    url="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle",
    author="Marina Baumgartner, Dairen Gonschior, Tilman Krummeck, "
    "Alexander Schwarz, Dennis Spitzhorn, Gerhard Trapp, Patrick Zwerschke",
    author_email="PS-TF-Entwicklung@tuev-sued.de",
    license="MIT",
    packages=[
        "qute_style",
        "qute_style.gen",
        "qute_style.dev",
        "qute_style.widgets",
    ],
    package_data={
        "qute_style": ["py.typed", "widgets/**/*.py"],
    },
    install_requires=["PySide6"],
    zip_safe=False,
)
