# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os,sys
import DynamicSolver
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.tripBuses = 0
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(519, 346)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.verticalTabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalTabWidget.sizePolicy().hasHeightForWidth())
        self.verticalTabWidget.setSizePolicy(sizePolicy)
        self.verticalTabWidget.setObjectName(_fromUtf8("verticalTabWidget"))
        self.solveTab = QtGui.QWidget()
        self.solveTab.setObjectName(_fromUtf8("solveTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.solveTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.solveTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.btnStudyDir = QtGui.QPushButton(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStudyDir.sizePolicy().hasHeightForWidth())
        self.btnStudyDir.setSizePolicy(sizePolicy)
        self.btnStudyDir.setObjectName(_fromUtf8("btnStudyDir"))
        self.horizontalLayout.addWidget(self.btnStudyDir)
        self.label_7 = QtGui.QLabel(self.solveTab)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.solveTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.btnCase = QtGui.QPushButton(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCase.sizePolicy().hasHeightForWidth())
        self.btnCase.setSizePolicy(sizePolicy)
        self.btnCase.setObjectName(_fromUtf8("btnCase"))
        self.horizontalLayout_2.addWidget(self.btnCase)
        self.label_8 = QtGui.QLabel(self.solveTab)
        self.label_8.setText(_fromUtf8(""))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_2.addWidget(self.label_8)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(self.solveTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.btnDyr = QtGui.QPushButton(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDyr.sizePolicy().hasHeightForWidth())
        self.btnDyr.setSizePolicy(sizePolicy)
        self.btnDyr.setObjectName(_fromUtf8("btnDyr"))
        self.horizontalLayout_5.addWidget(self.btnDyr)
        self.label_9 = QtGui.QLabel(self.solveTab)
        self.label_9.setText(_fromUtf8(""))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_5.addWidget(self.label_9)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.solveTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.btnDLL = QtGui.QPushButton(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDLL.sizePolicy().hasHeightForWidth())
        self.btnDLL.setSizePolicy(sizePolicy)
        self.btnDLL.setObjectName(_fromUtf8("btnDLL"))
        self.horizontalLayout_6.addWidget(self.btnDLL)
        self.label_10 = QtGui.QLabel(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_6.addWidget(self.label_10)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_5 = QtGui.QLabel(self.solveTab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.txtZoneNum = QtGui.QLineEdit(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtZoneNum.sizePolicy().hasHeightForWidth())
        self.txtZoneNum.setSizePolicy(sizePolicy)
        self.txtZoneNum.setObjectName(_fromUtf8("txtZoneNum"))
        self.horizontalLayout_3.addWidget(self.txtZoneNum)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_6 = QtGui.QLabel(self.solveTab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_4.addWidget(self.label_6)
        self.txtFault = QtGui.QLineEdit(self.solveTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtFault.sizePolicy().hasHeightForWidth())
        self.txtFault.setSizePolicy(sizePolicy)
        self.txtFault.setObjectName(_fromUtf8("txtFault"))
        self.horizontalLayout_4.addWidget(self.txtFault)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_11 = QtGui.QLabel(self.solveTab)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_7.addWidget(self.label_11)
        self.comboBoxTripType = QtGui.QComboBox(self.solveTab)
        self.comboBoxTripType.setObjectName(_fromUtf8("comboBoxTripType"))
        self.comboBoxTripType.addItem(_fromUtf8(""))
        self.comboBoxTripType.addItem(_fromUtf8(""))
        self.comboBoxTripType.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.comboBoxTripType)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_12 = QtGui.QLabel(self.solveTab)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_8.addWidget(self.label_12)
        self.txtFrom = QtGui.QLineEdit(self.solveTab)
        self.txtFrom.setObjectName(_fromUtf8("txtFrom"))
        self.horizontalLayout_8.addWidget(self.txtFrom)
        self.label_13 = QtGui.QLabel(self.solveTab)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_8.addWidget(self.label_13)
        self.txtTo1 = QtGui.QLineEdit(self.solveTab)
        self.txtTo1.setObjectName(_fromUtf8("txtTo1"))
        self.horizontalLayout_8.addWidget(self.txtTo1)
        self.label_14 = QtGui.QLabel(self.solveTab)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_14.setEnabled(False)
        self.horizontalLayout_8.addWidget(self.label_14)
        self.txtTo2 = QtGui.QLineEdit(self.solveTab)
        self.txtTo2.setObjectName(_fromUtf8("txtTo2"))
        self.txtTo2.setEnabled(False)
        self.horizontalLayout_8.addWidget(self.txtTo2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.pushButton = QtGui.QPushButton(self.solveTab)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_3.addWidget(self.pushButton)
        self.verticalTabWidget.addTab(self.solveTab, _fromUtf8(""))
        self.plotting = QtGui.QWidget()
        self.plotting.setObjectName(_fromUtf8("plotting"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.plotting)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_15 = QtGui.QLabel(self.plotting)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_4 = QtGui.QLineEdit(self.plotting)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_16 = QtGui.QLabel(self.plotting)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_16)
        self.lineEdit_5 = QtGui.QLineEdit(self.plotting)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_17 = QtGui.QLabel(self.plotting)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_17)
        self.lineEdit_6 = QtGui.QLineEdit(self.plotting)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_18 = QtGui.QLabel(self.plotting)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_18)
        self.checkBox = QtGui.QCheckBox(self.plotting)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.label_19 = QtGui.QLabel(self.plotting)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_19)
        self.checkBox_2 = QtGui.QCheckBox(self.plotting)
        self.checkBox_2.setText(_fromUtf8(""))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.checkBox_2)
        self.label_20 = QtGui.QLabel(self.plotting)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_20)
        self.checkBox_3 = QtGui.QCheckBox(self.plotting)
        self.checkBox_3.setText(_fromUtf8(""))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.checkBox_3)
        self.btnPlot = QtGui.QPushButton(self.plotting)
        self.btnPlot.setObjectName(_fromUtf8("btnPlot"))
        self.verticalLayout_4.addWidget(self.btnPlot)
        self.verticalTabWidget.addTab(self.plotting, _fromUtf8(""))
        self.horizontalLayout_9.addWidget(self.verticalTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.verticalTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Study Directory:", None))
        self.btnStudyDir.setText(_translate("MainWindow", "Select", None))
        self.label.setText(_translate("MainWindow", "Case File:", None))
        self.btnCase.setText(_translate("MainWindow", "Select", None))
        self.label_3.setText(_translate("MainWindow", "Dyr File:", None))
        self.btnDyr.setText(_translate("MainWindow", "Select", None))
        self.label_4.setText(_translate("MainWindow", "DLL File:", None))
        self.btnDLL.setText(_translate("MainWindow", "Select", None))
        self.label_5.setText(_translate("MainWindow", "Zone Number", None))
        self.label_6.setText(_translate("MainWindow", "Fault Bus Number", None))
        self.label_11.setText(_translate("MainWindow", "Trip:", None))
        self.comboBoxTripType.setItemText(0, _translate("MainWindow", "Branch", None))
        self.comboBoxTripType.setItemText(1, _translate("MainWindow", "Three winding Transformer", None))
        self.comboBoxTripType.setItemText(2, _translate("MainWindow", "Generation Unit", None))
        self.label_12.setText(_translate("MainWindow", "From", None))
        self.label_13.setText(_translate("MainWindow", "to", None))
        self.label_14.setText(_translate("MainWindow", "to", None))
        self.pushButton.setText(_translate("MainWindow", "Solve", None))
        self.verticalTabWidget.setTabText(self.verticalTabWidget.indexOf(self.solveTab), _translate("MainWindow", "Dynamic Run", None))
        self.label_15.setText(_translate("MainWindow", "Title:", None))
        self.label_16.setText(_translate("MainWindow", "Motors Buses", None))
        self.label_17.setText(_translate("MainWindow", "Voltages Buses", None))
        self.label_18.setText(_translate("MainWindow", "Frequency", None))
        self.label_19.setText(_translate("MainWindow", "SVC", None))
        self.label_20.setText(_translate("MainWindow", "Statcom", None))
        self.btnPlot.setText(_translate("MainWindow", "Plot", None))
        self.verticalTabWidget.setTabText(self.verticalTabWidget.indexOf(self.plotting), _translate("MainWindow", "Plotting", None))
    def on_StudyDir(self):
        self.dirpath = QtGui.QFileDialog.getExistingDirectory(MainWindow,'Select Folder', 'C:\\')
        self.label_7.setText(self.dirpath)
    def on_Solve(self):
        if self.txtZoneNum.text() == "":
            pass
        zone = int(self.txtZoneNum.text())
        fault = int(self.txtFault.text())
        self.triptype(self.comboBoxTripType.currentIndex())
        self.s = DynamicSolver.DynamicSolver(self.dirpath, self.dyrfile, self.dllfile, self.casefile, fault, zone, self.tripBuses,self.tripType)
        self.s.solve()
    def on_Plot(self):
        title = unicode(self.lineEdit_4.text(),encoding="UTF-8")
        motors = unicode(self.lineEdit_5.text(),encoding="UTF-8").split()
        volts = unicode(self.lineEdit_6.text(),encoding="UTF-8").split()
        bFreq = self.checkBox.isChecked()
        bSvc = self.checkBox_2.isChecked()
        bStatcom = self.checkBox_3.isChecked()
        self.s.plot(title,motors,volts,bFreq,bSvc,bStatcom)

    def on_Case(self):
        self.casefile = QtGui.QFileDialog.getOpenFileName(MainWindow,'Open File', 'C:\\')
        self.label_8.setText(self.casefile)
    def on_Dyr(self):
        self.dyrfile = QtGui.QFileDialog.getOpenFileName(MainWindow,'Open File', 'C:\\')
        self.label_9.setText(self.dyrfile)
    def on_DLL(self):
        self.dllfile = QtGui.QFileDialog.getOpenFileName(MainWindow,'Open File', 'C:\\')
        self.label_10.setText(self.dllfile)
    def triptype(self,i):
        f = self.txtFrom.text()
        t1 = self.txtTo1.text()
        t2 = self.txtTo2.text()
        if i == 1:
            self.tripType = 1
            # Three winding trip
            self.label_13.setEnabled(True)
            self.txtTo1.setEnabled(True)
            self.label_14.setEnabled(True)
            self.txtTo2.setEnabled(True)
            self.label_12.setText('From:')
            self.tripBuses = []
            self.tripBuses = [f, t1, t2]
        elif i == 2:
            self.tripType = 3
            # Trip Generation Unit
            self.label_13.setEnabled(False)
            self.txtTo1.setEnabled(False)
            self.label_12.setText('Generation Bus:')
            self.tripBuses = []
            self.tripBuses = [f]
        else:
            self.tripType = 3
            # Trip Branch
            self.label_13.setEnabled(True)
            self.txtTo1.setEnabled(True)
            self.label_14.setEnabled(False)
            self.txtTo2.setEnabled(False)
            self.label_12.setText('From:')
            self.tripBuses = []
            self.tripBuses = [f, t1]

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.btnStudyDir.pressed.connect(ui.on_StudyDir)
    ui.btnCase.pressed.connect(ui.on_Case)
    ui.btnDyr.pressed.connect(ui.on_Dyr)
    ui.btnDLL.pressed.connect(ui.on_DLL)
    ui.pushButton.pressed.connect(ui.on_Solve)
    ui.btnPlot.pressed.connect(ui.on_Plot)
    MainWindow.show()
    sys.exit(app.exec_())