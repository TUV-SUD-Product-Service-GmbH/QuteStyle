# QuteStyle

QuteStyle is an expandable application framework for PyQt5 and heavily inspired by [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6).
The main goal of this project is to provide a simple and easy to use application frame that can be used to create a new application.
It is mainly suited for applications that rely on a center widget that shows a selected widget from the left menu.

**Project status**

[![Python Versions](https://img.shields.io/badge/Python-3.8-blue.svg?&logo=Python&logoWidth=18&logoColor=white)](https://www.python.org/downloads/)
[![Qt Versions](https://img.shields.io/badge/Qt-5-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/github/license/TUV-SUD-Product-Service-GmbH/QuteStyle.svg?color=green)](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/blob/master/LICENSE/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)

## Features

- Easy integration of already existing widgets
- Preset themes that easily can be modified
- Custom widgets
- Splash screen
- Build-in release history
- Used and developed in a productive environment

## Themes

### Darcula Theme

# todo: add images

## Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Installation Method

- Latest development version

   ```plaintext
   pip install git+https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle.git@master
   ```

## Usage

```Python
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from examples.sample_main_window import StyledMainWindow
from qute_style.qs_application import QuteStyleApplication
from qute_style.update_window import AppData
import sys

class MyApplication(QuteStyleApplication):
    # take a look at examples.sample_main_window and examples.sample_widgets
    # to find out more about setting up a main window and the widgets that it
    # should display
    MAIN_WINDOW_CLASS = StyledMainWindow
    # add basic information about your application
    APP_DATA = AppData(
        "Test-App",
        "1.1.0",
        ":/svg_images/logo_toolbox.svg",
        ":/svg_images/logo_toolbox.svg",
        "",
    )

if __name__ == "__main__":

    APP_NAME = "Test-App"

    # activate highdpi icons and scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    APP = MyApplication(sys.argv)
    sys.exit(APP.exec())
```

## Example

Check out our example app by running:

```plaintext
python -m examples.main
```

## License

The original design idea is from [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6) (MIT License).
The svg files are derived from [Material design icons](https://fonts.google.com/icons) (Apache License Version 2.0). Other files are covered by QuteStyle's MIT license.

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.
