# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Draw_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Draw_btn.setGeometry(QtCore.QRect(50, 540, 120, 50))
        self.Draw_btn.setObjectName("Draw_btn")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 800, 540))
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, 798.0, 538.0))
        self.graphicsView.setObjectName("graphicsView")
        self.Shake_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Shake_btn.setGeometry(QtCore.QRect(170, 540, 120, 50))
        self.Shake_btn.setObjectName("Shake_btn")
        self.Clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Clear_btn.setGeometry(QtCore.QRect(290, 540, 120, 50))
        self.Clear_btn.setObjectName("Clear_btn")
        self.Count_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.Count_spinBox.setGeometry(QtCore.QRect(0, 540, 50, 50))
        self.Count_spinBox.setMinimum(1)
        self.Count_spinBox.setMaximum(50)
        self.Count_spinBox.setObjectName("Count_spinBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Draw_btn.setText(_translate("MainWindow", "Draw"))
        self.Shake_btn.setText(_translate("MainWindow", "Shake"))
        self.Clear_btn.setText(_translate("MainWindow", "Clear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
