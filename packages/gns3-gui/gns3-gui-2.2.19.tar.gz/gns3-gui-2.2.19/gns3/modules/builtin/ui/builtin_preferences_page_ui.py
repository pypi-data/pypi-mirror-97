# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/grossmj/PycharmProjects/gns3-gui/gns3/modules/builtin/ui/builtin_preferences_page.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BuiltinPreferencesPageWidget(object):
    def setupUi(self, BuiltinPreferencesPageWidget):
        BuiltinPreferencesPageWidget.setObjectName("BuiltinPreferencesPageWidget")
        BuiltinPreferencesPageWidget.resize(456, 385)
        self.verticalLayout = QtWidgets.QVBoxLayout(BuiltinPreferencesPageWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiTabWidget = QtWidgets.QTabWidget(BuiltinPreferencesPageWidget)
        self.uiTabWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.uiTabWidget.setObjectName("uiTabWidget")
        self.uiServerSettingsTabWidget = QtWidgets.QWidget()
        self.uiServerSettingsTabWidget.setObjectName("uiServerSettingsTabWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.uiServerSettingsTabWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.uiServerSettingsTabWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.uiNATInterfaceComboBox = QtWidgets.QComboBox(self.uiServerSettingsTabWidget)
        self.uiNATInterfaceComboBox.setObjectName("uiNATInterfaceComboBox")
        self.gridLayout.addWidget(self.uiNATInterfaceComboBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.uiTabWidget.addTab(self.uiServerSettingsTabWidget, "")
        self.verticalLayout.addWidget(self.uiTabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(254, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.uiRestoreDefaultsPushButton = QtWidgets.QPushButton(BuiltinPreferencesPageWidget)
        self.uiRestoreDefaultsPushButton.setObjectName("uiRestoreDefaultsPushButton")
        self.horizontalLayout_2.addWidget(self.uiRestoreDefaultsPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(BuiltinPreferencesPageWidget)
        self.uiTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BuiltinPreferencesPageWidget)

    def retranslateUi(self, BuiltinPreferencesPageWidget):
        _translate = QtCore.QCoreApplication.translate
        BuiltinPreferencesPageWidget.setWindowTitle(_translate("BuiltinPreferencesPageWidget", "Built-in"))
        self.label.setText(_translate("BuiltinPreferencesPageWidget", "Default NAT interface:"))
        self.uiTabWidget.setTabText(self.uiTabWidget.indexOf(self.uiServerSettingsTabWidget), _translate("BuiltinPreferencesPageWidget", "Local settings"))
        self.uiRestoreDefaultsPushButton.setText(_translate("BuiltinPreferencesPageWidget", "Restore defaults"))

