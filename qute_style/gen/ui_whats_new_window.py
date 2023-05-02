# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'whats_new_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class Ui_whats_new_window(object):
    def setupUi(self, whats_new_window):
        if not whats_new_window.objectName():
            whats_new_window.setObjectName("whats_new_window")
        whats_new_window.resize(389, 341)
        self.centralwidget = QWidget(whats_new_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 369, 249))
        self.horizontalLayout_3 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.text_label = QLabel(self.scrollAreaWidgetContents)
        self.text_label.setObjectName("text_label")
        self.text_label.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.text_label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.previous_button = QPushButton(self.centralwidget)
        self.previous_button.setObjectName("previous_button")

        self.horizontalLayout.addWidget(self.previous_button)

        self.next_button = QPushButton(self.centralwidget)
        self.next_button.setObjectName("next_button")

        self.horizontalLayout.addWidget(self.next_button)

        self.close_button = QPushButton(self.centralwidget)
        self.close_button.setObjectName("close_button")

        self.horizontalLayout.addWidget(self.close_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        whats_new_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(whats_new_window)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 389, 21))
        whats_new_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(whats_new_window)
        self.statusbar.setObjectName("statusbar")
        whats_new_window.setStatusBar(self.statusbar)

        self.retranslateUi(whats_new_window)

    # setupUi

    def retranslateUi(self, whats_new_window):
        whats_new_window.setWindowTitle(
            QCoreApplication.translate(
                "whats_new_window", "StyledMainWindow", None
            )
        )
        self.text_label.setText("")
        # if QT_CONFIG(tooltip)
        self.previous_button.setToolTip(
            QCoreApplication.translate(
                "whats_new_window", "Den letzten Eintrag anzeigen.", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.previous_button.setText(
            QCoreApplication.translate("whats_new_window", "Zur\u00fcck", None)
        )
        # if QT_CONFIG(tooltip)
        self.next_button.setToolTip(
            QCoreApplication.translate(
                "whats_new_window", "Den n\u00e4chsten Eintrag anzeigen.", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.next_button.setText(
            QCoreApplication.translate("whats_new_window", "Weiter", None)
        )
        # if QT_CONFIG(tooltip)
        self.close_button.setToolTip(
            QCoreApplication.translate(
                "whats_new_window",
                'Das Fenster schlie\u00dfen. Sie k\u00f6nnen das Fenster erneut anzeigen, indem Sie im Men\u00fc "Hilfe" den Eintrag "Neuerung" anw\u00e4hlen.',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.close_button.setText(
            QCoreApplication.translate(
                "whats_new_window", "Schlie\u00dfen", None
            )
        )

    # retranslateUi
