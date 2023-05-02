# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_window.ui'
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
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QDateTimeEdit,
    QDial,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollBar,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from qute_style.widgets.icon_button import IconButton
from qute_style.widgets.styled_combobox import StyledComboBox
from qute_style.widgets.toggle import Toggle
from qute_style_examples.sample_classes import (
    SelectAllTestComboBox,
    TestComboBox,
)


class Ui_test_widget(object):
    def setupUi(self, test_widget):
        if not test_widget.objectName():
            test_widget.setObjectName("test_widget")
        test_widget.resize(1219, 886)
        self.gridLayout_2 = QGridLayout(test_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QGroupBox(test_widget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEchoMode(QLineEdit.Normal)

        self.gridLayout.addWidget(self.lineEdit, 6, 0, 1, 2)

        self.horizontalScrollBar = QScrollBar(self.groupBox_3)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalScrollBar.setValue(25)
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalScrollBar, 10, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 11, 0, 1, 1)

        self.dateTimeEdit = QDateTimeEdit(self.groupBox_3)
        self.dateTimeEdit.setObjectName("dateTimeEdit")

        self.gridLayout.addWidget(self.dateTimeEdit, 8, 0, 1, 2)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.dial = QDial(self.groupBox_3)
        self.dial.setObjectName("dial")
        self.dial.setValue(30)

        self.gridLayout.addWidget(self.dial, 10, 0, 1, 1)

        self.styled_combobox = StyledComboBox(self.groupBox_3)
        self.styled_combobox.addItem("")
        self.styled_combobox.addItem("")
        self.styled_combobox.addItem("")
        self.styled_combobox.setObjectName("styled_combobox")

        self.gridLayout.addWidget(self.styled_combobox, 0, 1, 1, 1)

        self.transparent_combobox = StyledComboBox(self.groupBox_3)
        self.transparent_combobox.addItem("")
        self.transparent_combobox.addItem("")
        self.transparent_combobox.addItem("")
        self.transparent_combobox.setObjectName("transparent_combobox")

        self.gridLayout.addWidget(self.transparent_combobox, 3, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.checkable_combobox = TestComboBox(self.groupBox_3)
        self.checkable_combobox.setObjectName("checkable_combobox")

        self.gridLayout.addWidget(self.checkable_combobox, 1, 1, 1, 1)

        self.horizontalSlider = QSlider(self.groupBox_3)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(30)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.horizontalSlider, 11, 1, 1, 1)

        self.spinBox = QSpinBox(self.groupBox_3)
        self.spinBox.setObjectName("spinBox")

        self.gridLayout.addWidget(self.spinBox, 7, 0, 1, 2)

        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.comboBox = SelectAllTestComboBox(self.groupBox_3)
        self.comboBox.setObjectName("comboBox")

        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)

        self.gridLayout_2.addWidget(self.groupBox_3, 4, 1, 1, 1)

        self.groupBox_2 = QGroupBox(test_widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = IconButton(self.groupBox_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFlat(False)

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.pushButton_4 = IconButton(self.groupBox_2)
        self.pushButton_4.setObjectName("pushButton_4")

        self.verticalLayout_3.addWidget(self.pushButton_4)

        self.gridLayout_2.addWidget(self.groupBox_2, 2, 1, 1, 1)

        self.groupBox = QGroupBox(test_widget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setToolTipDuration(-10)
        self.radioButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")

        self.verticalLayout_5.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName("radioButton_3")

        self.verticalLayout_5.addWidget(self.radioButton_3)

        self.checkBox_5 = QCheckBox(self.groupBox)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.setTristate(True)

        self.verticalLayout_5.addWidget(self.checkBox_5)

        self.custom_icon_engine_checkbox = QCheckBox(self.groupBox)
        self.custom_icon_engine_checkbox.setObjectName(
            "custom_icon_engine_checkbox"
        )

        self.verticalLayout_5.addWidget(self.custom_icon_engine_checkbox)

        self.icon_checkbox = QCheckBox(self.groupBox)
        self.icon_checkbox.setObjectName("icon_checkbox")

        self.verticalLayout_5.addWidget(self.icon_checkbox)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_3 = Toggle(self.groupBox)
        self.checkBox_3.setObjectName("checkBox_3")

        self.horizontalLayout_5.addWidget(self.checkBox_3)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.checkBox_4 = Toggle(self.groupBox)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_5.addWidget(self.checkBox_4)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox = Toggle(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setAutoExclusive(False)

        self.horizontalLayout_4.addWidget(self.checkBox)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.checkBox_2 = Toggle(self.groupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_4.addWidget(self.checkBox_2)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.disable_widgets = QCheckBox(test_widget)
        self.disable_widgets.setObjectName("disable_widgets")
        font = QFont()
        font.setFamilies(["Segoe UI"])
        self.disable_widgets.setFont(font)
        self.disable_widgets.setChecked(False)

        self.horizontalLayout.addWidget(self.disable_widgets)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.progressBar = QProgressBar(test_widget)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(30)

        self.gridLayout_2.addWidget(self.progressBar, 6, 0, 1, 2)

        self.tabWidget = QTabWidget(test_widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QTextEdit(self.tab)
        self.textEdit.setObjectName("textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QTableWidget(self.tab_2)
        if self.tableWidget.columnCount() < 10:
            self.tableWidget.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        if self.tableWidget.rowCount() < 10:
            self.tableWidget.setRowCount(10)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget.setItem(0, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem22)
        self.tableWidget.setObjectName("tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tab_3.setCursor(QCursor(Qt.ArrowCursor))
        self.horizontalLayout_2 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QSplitter(self.tab_3)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter_label = QLabel(self.splitter)
        self.splitter_label.setObjectName("splitter_label")
        self.splitter.addWidget(self.splitter_label)
        self.splitter_button = QPushButton(self.splitter)
        self.splitter_button.setObjectName("splitter_button")
        self.splitter.addWidget(self.splitter_button)

        self.horizontalLayout_2.addWidget(self.splitter)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_6 = QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.drop_widget = QTreeWidget(self.tab_4)
        self.drop_widget.setObjectName("drop_widget")
        self.drop_widget.setAcceptDrops(True)
        self.drop_widget.setDragEnabled(True)
        self.drop_widget.setDragDropMode(QAbstractItemView.DragDrop)

        self.verticalLayout_6.addWidget(self.drop_widget)

        self.clear_drop_button = QPushButton(self.tab_4)
        self.clear_drop_button.setObjectName("clear_drop_button")

        self.verticalLayout_6.addWidget(self.clear_drop_button)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.treeWidget = QTreeWidget(self.tab_6)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName("treeWidget")

        self.verticalLayout_7.addWidget(self.treeWidget)

        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.tab_6, "")

        self.gridLayout_2.addWidget(self.tabWidget, 4, 0, 1, 1)

        self.retranslateUi(test_widget)

        self.pushButton_4.setDefault(False)
        self.tabWidget.setCurrentIndex(4)

    # setupUi

    def retranslateUi(self, test_widget):
        test_widget.setWindowTitle(
            QCoreApplication.translate("test_widget", "Form", None)
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate("test_widget", "GroupBox", None)
        )
        self.lineEdit.setText(
            QCoreApplication.translate("test_widget", "test", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "test_widget", "Test QProgressBar:", None
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "test_widget", "Transparent ComboBox", None
            )
        )
        self.styled_combobox.setItemText(
            0, QCoreApplication.translate("test_widget", "New Item", None)
        )
        self.styled_combobox.setItemText(
            1, QCoreApplication.translate("test_widget", "New Item 2", None)
        )
        self.styled_combobox.setItemText(
            2, QCoreApplication.translate("test_widget", "New Item 3", None)
        )

        self.transparent_combobox.setItemText(
            0, QCoreApplication.translate("test_widget", "New Item", None)
        )
        self.transparent_combobox.setItemText(
            1, QCoreApplication.translate("test_widget", "New Item 2", None)
        )
        self.transparent_combobox.setItemText(
            2, QCoreApplication.translate("test_widget", "New Item 3", None)
        )

        self.label_4.setText(
            QCoreApplication.translate(
                "test_widget", "Checkable ComboBox", None
            )
        )
        self.label.setText(
            QCoreApplication.translate("test_widget", "Styled ComboBox", None)
        )
        self.label_5.setText(
            QCoreApplication.translate(
                "test_widget", "SelectAll ComboBox", None
            )
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("test_widget", "GroupBox", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("test_widget", "PushButton", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("test_widget", "PushButton", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("test_widget", "Test-Text", None)
        )
        self.pushButton_4.setText("")
        self.groupBox.setTitle(
            QCoreApplication.translate("test_widget", "GroupBox", None)
        )
        self.radioButton.setText(
            QCoreApplication.translate("test_widget", "RadioButton", None)
        )
        self.radioButton_2.setText(
            QCoreApplication.translate("test_widget", "RadioButton", None)
        )
        self.radioButton_3.setText(
            QCoreApplication.translate("test_widget", "RadioButton", None)
        )
        self.checkBox_5.setText(
            QCoreApplication.translate("test_widget", "CheckBox", None)
        )
        self.custom_icon_engine_checkbox.setText(
            QCoreApplication.translate(
                "test_widget", "Checkbox with CustomIconEngine", None
            )
        )
        self.icon_checkbox.setText(
            QCoreApplication.translate(
                "test_widget", "CheckBox with QIcon", None
            )
        )
        self.checkBox_3.setText(
            QCoreApplication.translate(
                "test_widget",
                "This is a very long test text so that we can crop",
                None,
            )
        )
        self.checkBox_4.setText(
            QCoreApplication.translate("test_widget", "CheckBox", None)
        )
        self.checkBox.setText("")
        self.checkBox_2.setText("")
        self.disable_widgets.setText(
            QCoreApplication.translate("test_widget", "Disable Widgets", None)
        )
        self.textEdit.setHtml(
            QCoreApplication.translate(
                "test_widget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'.SF NS Text\'; font-size:13pt;">test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />'
                "test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br /></span></p></body></html>",
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            QCoreApplication.translate("test_widget", "TextEdit", None),
        )
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("test_widget", "1", None)
        )
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("test_widget", "2", None)
        )
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("test_widget", "3", None)
        )
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("test_widget", "4", None)
        )
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("test_widget", "5", None)
        )
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("test_widget", "6", None)
        )
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("test_widget", "7", None)
        )
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(
            QCoreApplication.translate("test_widget", "8", None)
        )
        ___qtablewidgetitem8 = self.tableWidget.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(
            QCoreApplication.translate("test_widget", "9", None)
        )
        ___qtablewidgetitem9 = self.tableWidget.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(
            QCoreApplication.translate("test_widget", "10", None)
        )
        ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem10.setText(
            QCoreApplication.translate("test_widget", "1", None)
        )
        ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(1)
        ___qtablewidgetitem11.setText(
            QCoreApplication.translate("test_widget", "2", None)
        )
        ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(2)
        ___qtablewidgetitem12.setText(
            QCoreApplication.translate("test_widget", "3", None)
        )
        ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(3)
        ___qtablewidgetitem13.setText(
            QCoreApplication.translate("test_widget", "4", None)
        )
        ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(4)
        ___qtablewidgetitem14.setText(
            QCoreApplication.translate("test_widget", "5", None)
        )
        ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(5)
        ___qtablewidgetitem15.setText(
            QCoreApplication.translate("test_widget", "6", None)
        )
        ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(6)
        ___qtablewidgetitem16.setText(
            QCoreApplication.translate("test_widget", "7", None)
        )
        ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(7)
        ___qtablewidgetitem17.setText(
            QCoreApplication.translate("test_widget", "8", None)
        )
        ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(8)
        ___qtablewidgetitem18.setText(
            QCoreApplication.translate("test_widget", "9", None)
        )
        ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(9)
        ___qtablewidgetitem19.setText(
            QCoreApplication.translate("test_widget", "10", None)
        )

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem20 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem20.setText(
            QCoreApplication.translate("test_widget", "Milben Power", None)
        )
        ___qtablewidgetitem21 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem21.setText(
            QCoreApplication.translate("test_widget", "Milben Power", None)
        )
        ___qtablewidgetitem22 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem22.setText(
            QCoreApplication.translate("test_widget", "Miben Power", None)
        )
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            QCoreApplication.translate("test_widget", "Tab Table", None),
        )
        self.splitter_label.setText(
            QCoreApplication.translate("test_widget", "TextLabel", None)
        )
        self.splitter_button.setText(
            QCoreApplication.translate("test_widget", "PushButton", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            QCoreApplication.translate("test_widget", "QSplitter", None),
        )
        ___qtreewidgetitem = self.drop_widget.headerItem()
        ___qtreewidgetitem.setText(
            0, QCoreApplication.translate("test_widget", "Test Files", None)
        )
        self.clear_drop_button.setText(
            QCoreApplication.translate("test_widget", "Clear", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4),
            QCoreApplication.translate("test_widget", "DropArea", None),
        )
        ___qtreewidgetitem1 = self.treeWidget.headerItem()
        ___qtreewidgetitem1.setText(
            0, QCoreApplication.translate("test_widget", "1", None)
        )

        __sortingEnabled1 = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem2.setText(
            0, QCoreApplication.translate("test_widget", "Item 1", None)
        )
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(
            0, QCoreApplication.translate("test_widget", "Subitem", None)
        )
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(
            0, QCoreApplication.translate("test_widget", "SubSub", None)
        )
        ___qtreewidgetitem5 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem5.setText(
            0, QCoreApplication.translate("test_widget", "Item 2", None)
        )
        self.treeWidget.setSortingEnabled(__sortingEnabled1)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_6),
            QCoreApplication.translate("test_widget", "TreeView", None),
        )

    # retranslateUi
