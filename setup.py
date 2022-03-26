"""Setup script for QuteStyle library."""
from setuptools import setup

from qute_style.version import VERSION

setup(
    name="qute_style",
    version=VERSION,
    description="An expandable application framework for Qt",
    url="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle",
    author="Marina Baumgartner, Dairen Gonschior, Tilman Krummeck, "
    "Gerhard Trapp, Patrick Zwerschke",
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
    install_requires=[
        "PyQt5",
        "QtWaitingSpinner @ git+https://github.com/z3ntu/QtWaitingSpinner.git",
    ],
    zip_safe=False,
)
