# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qute_style\ui\test_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_test_widget(object):
    def setupUi(self, test_widget):
        test_widget.setObjectName("test_widget")
        test_widget.resize(1219, 886)
        self.gridLayout_2 = QtWidgets.QGridLayout(test_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(test_widget)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_3)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 30)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 9, 1, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 5, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.groupBox_3)
        self.horizontalScrollBar.setProperty("value", 25)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.gridLayout.addWidget(self.horizontalScrollBar, 8, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 4, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.dial = QtWidgets.QDial(self.groupBox_3)
        self.dial.setProperty("value", 30)
        self.dial.setObjectName("dial")
        self.gridLayout.addWidget(self.dial, 8, 0, 1, 1)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.groupBox_3)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.gridLayout.addWidget(self.dateTimeEdit, 6, 0, 1, 2)
        self.transparent_combobox = StyledComboBox(self.groupBox_3)
        self.transparent_combobox.setObjectName("transparent_combobox")
        self.transparent_combobox.addItem("")
        self.transparent_combobox.addItem("")
        self.transparent_combobox.addItem("")
        self.gridLayout.addWidget(self.transparent_combobox, 2, 1, 1, 1)
        self.styled_combobox = StyledComboBox(self.groupBox_3)
        self.styled_combobox.setObjectName("styled_combobox")
        self.styled_combobox.addItem("")
        self.styled_combobox.addItem("")
        self.styled_combobox.addItem("")
        self.gridLayout.addWidget(self.styled_combobox, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.checkable_combobox = TestComboBox(self.groupBox_3)
        self.checkable_combobox.setObjectName("checkable_combobox")
        self.gridLayout.addWidget(self.checkable_combobox, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 4, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(test_widget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = IconButton(self.groupBox_2)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.pushButton_4 = IconButton(self.groupBox_2)
        self.pushButton_4.setText("")
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.gridLayout_2.addWidget(self.groupBox_2, 2, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(test_widget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setToolTipDuration(-10)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_5.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_5.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_5.addWidget(self.radioButton_3)
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setTristate(True)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_5.addWidget(self.checkBox_5)
        self.custom_icon_engine_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.custom_icon_engine_checkbox.setObjectName(
            "custom_icon_engine_checkbox"
        )
        self.verticalLayout_5.addWidget(self.custom_icon_engine_checkbox)
        self.icon_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.icon_checkbox.setObjectName("icon_checkbox")
        self.verticalLayout_5.addWidget(self.icon_checkbox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_3 = Toggle(self.groupBox)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_5.addWidget(self.checkBox_3)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_5.addItem(spacerItem1)
        self.checkBox_4 = Toggle(self.groupBox)
        self.checkBox_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_5.addWidget(self.checkBox_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox = Toggle(self.groupBox)
        self.checkBox.setText("")
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setAutoExclusive(False)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_4.addWidget(self.checkBox)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_4.addItem(spacerItem2)
        self.checkBox_2 = Toggle(self.groupBox)
        self.checkBox_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_4.addWidget(self.checkBox_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(test_widget)
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(10)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tab_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter_label = QtWidgets.QLabel(self.splitter)
        self.splitter_label.setObjectName("splitter_label")
        self.splitter_button = QtWidgets.QPushButton(self.splitter)
        self.splitter_button.setObjectName("splitter_button")
        self.horizontalLayout_2.addWidget(self.splitter)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.drop_widget = QtWidgets.QTreeWidget(self.tab_4)
        self.drop_widget.setAcceptDrops(True)
        self.drop_widget.setDragEnabled(True)
        self.drop_widget.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.drop_widget.setObjectName("drop_widget")
        self.verticalLayout_6.addWidget(self.drop_widget)
        self.clear_drop_button = QtWidgets.QPushButton(self.tab_4)
        self.clear_drop_button.setObjectName("clear_drop_button")
        self.verticalLayout_6.addWidget(self.clear_drop_button)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_2.addWidget(self.tabWidget, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.disable_widgets = QtWidgets.QCheckBox(test_widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.disable_widgets.setFont(font)
        self.disable_widgets.setChecked(False)
        self.disable_widgets.setObjectName("disable_widgets")
        self.horizontalLayout.addWidget(self.disable_widgets)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(test_widget)
        self.progressBar.setProperty("value", 30)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 6, 0, 1, 2)

        self.retranslateUi(test_widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(test_widget)

    def retranslateUi(self, test_widget):
        _translate = QtCore.QCoreApplication.translate
        test_widget.setWindowTitle(_translate("test_widget", "Form"))
        self.groupBox_3.setTitle(_translate("test_widget", "GroupBox"))
        self.label.setText(_translate("test_widget", "Styled ComboBox"))
        self.label_3.setText(_translate("test_widget", "Test QProgressBar:"))
        self.lineEdit.setText(_translate("test_widget", "test"))
        self.label_2.setText(_translate("test_widget", "Transparent ComboBox"))
        self.transparent_combobox.setItemText(
            0, _translate("test_widget", "New Item")
        )
        self.transparent_combobox.setItemText(
            1, _translate("test_widget", "New Item 2")
        )
        self.transparent_combobox.setItemText(
            2, _translate("test_widget", "New Item 3")
        )
        self.styled_combobox.setItemText(
            0, _translate("test_widget", "New Item")
        )
        self.styled_combobox.setItemText(
            1, _translate("test_widget", "New Item 2")
        )
        self.styled_combobox.setItemText(
            2, _translate("test_widget", "New Item 3")
        )
        self.label_4.setText(_translate("test_widget", "Checkable ComboBox"))
        self.groupBox_2.setTitle(_translate("test_widget", "GroupBox"))
        self.pushButton.setText(_translate("test_widget", "PushButton"))
        self.pushButton_2.setText(_translate("test_widget", "PushButton"))
        self.pushButton_3.setText(_translate("test_widget", "Test-Text"))
        self.groupBox.setTitle(_translate("test_widget", "GroupBox"))
        self.radioButton.setText(_translate("test_widget", "RadioButton"))
        self.radioButton_2.setText(_translate("test_widget", "RadioButton"))
        self.radioButton_3.setText(_translate("test_widget", "RadioButton"))
        self.checkBox_5.setText(_translate("test_widget", "CheckBox"))
        self.custom_icon_engine_checkbox.setText(
            _translate("test_widget", "Checkbox with CustomIconEngine")
        )
        self.icon_checkbox.setText(
            _translate("test_widget", "CheckBox with QIcon")
        )
        self.checkBox_3.setText(
            _translate(
                "test_widget",
                "This is a very long test text so that we can crop",
            )
        )
        self.checkBox_4.setText(_translate("test_widget", "CheckBox"))
        self.textEdit.setHtml(
            _translate(
                "test_widget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'.SF NS Text\'; font-size:13pt;">test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br />test<br /></span></p></body></html>',
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            _translate("test_widget", "TextEdit"),
        )
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("test_widget", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("test_widget", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("test_widget", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("test_widget", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("test_widget", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("test_widget", "6"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("test_widget", "7"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("test_widget", "8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("test_widget", "9"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("test_widget", "10"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("test_widget", "1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("test_widget", "2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("test_widget", "3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("test_widget", "4"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("test_widget", "5"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("test_widget", "6"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("test_widget", "7"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("test_widget", "8"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("test_widget", "9"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("test_widget", "10"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("test_widget", "Milben Power"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("test_widget", "Milben Power"))
        item = self.tableWidget.item(1, 0)
        item.setText(_translate("test_widget", "Miben Power"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            _translate("test_widget", "Tab Table"),
        )
        self.splitter_label.setText(_translate("test_widget", "TextLabel"))
        self.splitter_button.setText(_translate("test_widget", "PushButton"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3),
            _translate("test_widget", "QSplitter"),
        )
        self.drop_widget.headerItem().setText(
            0, _translate("test_widget", "Test Files")
        )
        self.clear_drop_button.setText(_translate("test_widget", "Clear"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4),
            _translate("test_widget", "DropArea"),
        )
        self.disable_widgets.setText(
            _translate("test_widget", "Disable Widgets")
        )


from examples.sample_classes import TestComboBox
from qute_style.widgets.icon_button import IconButton
from qute_style.widgets.styled_combobox import StyledComboBox
from qute_style.widgets.toggle import Toggle
