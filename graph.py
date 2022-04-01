# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, \
    QGraphicsSceneDragDropEvent, QGraphicsSceneHoverEvent, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF, QPoint
import random
import numpy as np


def get_coord(point):
    return np.array([point.x(), point.y()])


class Field(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, field, parent):
        self.value = field
        super().__init__(x - field / 2, y - field / 2, w + field, h + field, parent=parent)
        self.parent = parent

    def get_parent(self):
        return self.parent


class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h)
        self.font = QFont("Times", 20, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)

    def mousePressEvent(self, event):
        print('Press')
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print('Release')
        super(Node, self).mouseReleaseEvent(event)

    def get_pos(self):
        return self.x(), self.y()



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
        self.Draw_btn.clicked.connect(lambda: self.draw_nodes())
        self.Clear_btn.clicked.connect(lambda: self.clear())
        self.Shake_btn.clicked.connect(lambda: self.move_nodes())

    def draw_node(self, x, y, text):
        node = Node(0, 0, 50, 50, text)
        node.setPos(x, y)
        node.setBrush(QBrush(Qt.red))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)

    def draw_nodes(self):
        self.clear()
        count = 0
        for i in range(self.Count_spinBox.value()):
            x = random.randint(0, 748)
            y = random.randint(0, 488)
            self.draw_node(x, y, str(count))
            print('node: ' + str(count) + ' x: ' + str(x) + ' y : ' + str(y))
            count += 1

        # координаты
        # print(list(map(get_coord, self.scene.items())))

        # растояние
        # print(self.items_distance())

        # items_rep
        # print('repr')
        # print(self.items_repr())

        # items_spring
        # print('spring')
        # print(self.items_spring())

        # unit_vectors
        # print('unit_vectors')
        # print(self.unit_vectors())

        # print('power')
        # print(self.move_nodes())

    def clear(self):
        self.scene.clear()

    def items_distance(self):
        nodes = [x for x in self.scene.items() if isinstance(x, Node)]
        points = list(map(get_coord, nodes))
        length = len(nodes)
        distance = np.ones((length, length))
        for i in range(length):
            for j in range(length):
                distance[i][j] = np.linalg.norm(points[i] - points[j])
        return distance

    def unit_vectors(self):
        nodes = [x for x in self.scene.items() if isinstance(x, Node)]
        points = list(map(get_coord, nodes))
        length = len(nodes)
        distance = self.items_distance()
        units = np.ones((length, length, 2))
        for i in range(length):
            for j in range(length):
                if distance[i][j] == 0:
                    units[i][j] = [0., 0.]
                else:
                    units[i][j] = (points[i] - points[j]) / distance[i][j]
        return units

    def items_spring(self):
        distance = self.items_distance()
        repr = np.ones(distance.shape)
        l = np.sqrt(self.width * self.height / len(self.nodes_coords()))
        # print('l_repr')
        # print(l)
        for i in range(distance.shape[0]):
            for j in range(distance.shape[0]):
                repr[i][j] = (distance[i][j] ** 2) / l
        return repr

    def items_repr(self):
        distance = self.items_distance()
        spring = np.ones(distance.shape)
        l = np.sqrt(self.width * self.height / len(self.nodes_coords()))
        # print('l_spring')
        # print(l)
        for i in range(distance.shape[0]):
            for j in range(distance.shape[0]):
                if distance[i][j] == 0:
                    spring[i][j] = 0.
                else:
                    spring[i][j] = (l ** 2) / distance[i][j]
        return spring

    def nodes_coords(self):
        nodes = [x for x in self.scene.items() if isinstance(x, Node)]
        points = list(map(get_coord, nodes))
        return points

    def move_nodes(self):
        points = self.nodes_coords()
        units = self.unit_vectors()
        power = self.items_repr() - self.items_spring()
        vectors = np.ones(units.shape)

        for i in range(units.shape[0]):
            for j in range(units.shape[0]):
                vectors[i][j] = power[i][j] * units[i][j]
        vectors = np.sum(vectors, axis=0)

        self.clear()
        count = 0
        for i in range(len(points)):
            # print('point ' + str(count))
            # print('old x y')
            # print(points[i])
            # print('vectors')
            # print(vectors[i])
            x = points[i][0] + vectors[i][0]
            y = points[i][1] + vectors[i][1]
            if x < 0:
                x = 0
            if y < 0:
                 y = 0
            if x > 748:
                x = 748
            if y > 488:
                y = 488
            # print('new x y')
            # print((x, y))
            self.draw_node(x, y, str(count))
            count += 1
        #return vectors


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
