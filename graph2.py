# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsTextItem, QGraphicsItem
from Node import *
import random
import numpy as np


def get_coord(point):
    return np.array([point.x(), point.y()])


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
        self.width = 798.0
        self.height = 538.0
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, self.width, self.height))
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
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
        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Draw_btn.setText(_translate("MainWindow", "Draw"))
        self.Shake_btn.setText(_translate("MainWindow", "Shake"))
        self.Clear_btn.setText(_translate("MainWindow", "Clear"))

    def add_functions(self):
        self.Draw_btn.clicked.connect(lambda: self.draw_random_nodes())
        self.Shake_btn.clicked.connect(lambda: self.forces(1))
        self.Clear_btn.clicked.connect(lambda: self.test())

    def get_nodes(self):
        nodes = [item for item in self.scene.items() if isinstance(item, Node)]
        nodes.reverse()
        return nodes

    def get_nodes_coord(self):
        nodes = self.get_nodes()
        coord = list(map(get_coord, nodes))
        return np.array(coord)

    def draw_node(self, x, y, text):
        node = Node(0, 0, 50, 50, text)
        node.setPos(x, y)
        node.setBrush(QBrush(Qt.red))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)

    def draw_nodes(self, coord_array):
        self.scene.clear()
        count = 0
        for coord in coord_array:
            self.draw_node(coord[0], coord[1], str(count))
            count += 1

    def draw_random_nodes(self):
        coord_array = []
        for i in range(self.Count_spinBox.value()):
            x = random.randint(0, int(self.width - 30))
            y = random.randint(0, int(self.height - 30))
            coord_array.append([x, y])
        self.draw_nodes(np.array(coord_array))
        print(np.array(coord_array))

    def distance(self):
        points = self.get_nodes_coord()
        length = len(points)
        distance = np.ones((length, length))
        for i in range(length):
            for j in range(length):
                distance[i][j] = np.linalg.norm(points[i] - points[j])
        return distance

    def attractive_forces(self, c):
        distance = self.distance()
        attractive = np.ones(distance.shape)
        l = c * np.sqrt(self.width * self.height / len(self.get_nodes()))
        for i in range(distance.shape[0]):
            for j in range(distance.shape[0]):
                attractive[i][j] = (distance[i][j] ** 2) / l
        return attractive

    def repulsive_forces(self, c):
        distance = self.distance()
        repulsive = np.ones(distance.shape)
        l = c * np.sqrt(self.width * self.height / len(self.get_nodes()))
        for i in range(distance.shape[0]):
            for j in range(distance.shape[0]):
                if distance[i][j] == 0:
                    repulsive[i][j] = 0.
                else:
                    repulsive[i][j] = (l ** 2) / distance[i][j]
        return repulsive

    def forces(self, c):
        return self.attractive_forces(c) - self.repulsive_forces(c)

    def unit_vectors(self):
        points = self.get_nodes_coord()
        length = len(points)
        distance = self.distance()
        units = np.ones((length, length, 2))
        for i in range(length):
            for j in range(length):
                if distance[i][j] == 0:
                    units[i][j] = [0., 0.]
                else:
                    units[i][j] = (points[i] - points[j]) / distance[i][j]
        return units

    def test(self):
        forces = np.sum(self.forces(1), axis=0)
        forces_sign = forces/np.absolute(forces)
        vectors = np.sum(self.unit_vectors(), axis=0)
        old_coord = self.get_nodes_coord()
        new_coord = np.ones(old_coord.shape)
        for i in range(old_coord.shape[0]):
            new_coord[i] = old_coord[i] + (forces_sign[i] * vectors[i])
        self.draw_nodes(new_coord)
        print(forces)
        print(forces/np.absolute(forces))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
