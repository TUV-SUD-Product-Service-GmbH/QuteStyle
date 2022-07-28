<p align="center">
  <a href="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle">
    <img src="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/raw/master/qute_style/resources/svg_images/banner_qute_style.svg" alt="QuteStyle logo" width="500" height="200">
  </a>
</p>

# QuteStyle

QuteStyle is an expandable application framework for PyQt5 and heavily inspired by [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6).
The main goal of this project is to provide a simple and easy to use application frame that can be used to create a new application.
It is mainly suited for applications that rely on a center widget for user interaction. Functionality is extendable by having different widgets that can be loaded into that center widget area.

**Project status**

[![Python Versions](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10-blue.svg?&logo=Python&logoWidth=18&logoColor=white)](https://www.python.org/downloads/)
[![Qt Versions](https://img.shields.io/badge/Qt-5-blue.svg?&logo=Qt&logoWidth=18&logoColor=white)](https://www.qt.io/qt-for-python)
[![License](https://img.shields.io/github/license/TUV-SUD-Product-Service-GmbH/QuteStyle.svg)](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/python/black)

**Tests**

[![CodeQL](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/workflows/CodeQL/badge.svg)](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/actions?query=workflow%3ACodeQL)
[![Build Status](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/workflows/Tests/badge.svg?branch=master&event=push)](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/actions?query=workflow%3ATests)
[![Code Coverage](https://codecov.io/github/TUV-SUD-Product-Service-GmbH/QuteStyle/coverage.svg?branch=master&token=)](https://codecov.io/gh/TUV-SUD-Product-Service-GmbH/QuteStyle)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TUV-SUD-Product-Service-GmbH/QuteStyle/master.svg)](https://results.pre-commit.ci/latest/github/TUV-SUD-Product-Service-GmbH/QuteStyle/master)

## Features

- Easy integration of already existing widgets
- Preset themes that easily can be modified
- Custom widgets
- Splash screen
- Build-in release history
- Used and developed in a productive environment

## Themes and Styled Widgets

QuteStyle provides five themes, defining the color composition of the app.
Additionally, the user can define new themes ([check this out](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/blob/master/docs/style.md)). We provide five themes, for example a dark and light mode ```Darcula``` and ```Highbridge Grey```.
We defined [custom widgets](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/blob/master/docs/widgets.md), such that they fit to the overall style and implemented new behaviour. A selection can be found in the Test-App:

<img src="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/raw/master/examples/example_images/highbridge_grey.PNG" alt="Highbridge Grey" width="400" height="300"><img src="https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/raw/master/examples/example_images/darcula.PNG" alt="Darcula" width="400" height="300">


## Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Installation Method

- Latest development version

   ```plaintext
   pip install qute-style
   ```

## Usage

```Python
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from examples.sample_main_window import StyledMainWindow
from qute_style.qs_application import QuteStyleApplication
from qute_style.update_window import AppData

class MyApplication(QuteStyleApplication):
    # take a look at examples.sample_main_window and examples.sample_widgets
    # to find out more about setting up a main window and the widgets that it
    # should display
    MAIN_WINDOW_CLASS = StyledMainWindow
    # add basic information about your application
    APP_DATA = AppData(
        "Test-App",
        "2.3.4",
        ":/svg_images/logo_qute_style.svg",
        ":/svg_images/logo_qute_style.svg",
        "",
        "Test Version",
    )

if __name__ == "__main__":

    APP_NAME = "Test-App"

    # activate highdpi icons and scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    APP = MyApplication(sys.argv)
    sys.exit(APP.exec())
```

For further information, see our [documentation](https://github.com/TUV-SUD-Product-Service-GmbH/QuteStyle/tree/master/docs).

## Example

Check out our example app by running:

```plaintext
python -m examples.main
```

## License

The original design idea is from [Wanderson-Magalhaes](https://github.com/Wanderson-Magalhaes) and his project [PyDracula](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6) (MIT License).
The svg files are derived from [Material design icons](https://fonts.google.com/icons) (Apache License Version 2.0). Other files are covered by QuteStyle's MIT license.

## Contributing

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.
