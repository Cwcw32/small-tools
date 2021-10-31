# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(983, 465)
        self.O = QtWidgets.QPushButton(Dialog)
        self.O.setGeometry(QtCore.QRect(180, 360, 158, 54))
        self.O.setObjectName("O")
        self.C = QtWidgets.QPushButton(Dialog)
        self.C.setGeometry(QtCore.QRect(650, 360, 158, 54))
        self.C.setObjectName("C")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(189, 70, 681, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ak = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.ak.setText("")
        self.ak.setObjectName("ak")
        self.verticalLayout.addWidget(self.ak)
        self.sk = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.sk.setText("")
        self.sk.setObjectName("sk")
        self.verticalLayout.addWidget(self.sk)
        self.region = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.region.setText("")
        self.region.setObjectName("region")
        self.verticalLayout.addWidget(self.region)
        self.pid = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.pid.setText("")
        self.pid.setObjectName("pid")
        self.verticalLayout.addWidget(self.pid)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(49, 70, 401, 251))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.a = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.a.setObjectName("a")
        self.verticalLayout_2.addWidget(self.a)
        self.b = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.b.setObjectName("b")
        self.verticalLayout_2.addWidget(self.b)
        self.a_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.a_2.setObjectName("a_2")
        self.verticalLayout_2.addWidget(self.a_2)
        self.sk_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.sk_2.setObjectName("sk_2")
        self.verticalLayout_2.addWidget(self.sk_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.O.setText(_translate("Dialog", "OK"))
        self.C.setText(_translate("Dialog", "Cancel"))
        self.a.setText(_translate("Dialog", "AK"))
        self.b.setText(_translate("Dialog", "SK"))
        self.a_2.setText(_translate("Dialog", "Region"))
        self.sk_2.setText(_translate("Dialog", "Project_id"))

