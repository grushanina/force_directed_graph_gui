# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


import random

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem


from FamilyTree import *

def str_to_matrix(string):
    result = []
    matrix_string = string[1:-1]
    for row in matrix_string.split('\n '):
        cur_row = np.array(row[1:-1].split(' ')).astype(int)
        result.append(cur_row)
    return np.array(result)


def get_coord(point):
    return np.array([point.x(), point.y()])


class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, text, parent):
        super().__init__(x, y, w, h)
        self.font = QFont("Times", 20, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)
        self.parent = parent

    def mousePressEvent(self, event):
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(Node, self).mouseReleaseEvent(event)
        coords = self.parent.get_nodes_coord()
        self.parent.scene.clear()
        self.parent.draw_edges(coords)
        self.parent.draw_nodes(coords)

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
        self.Count_spinBox.setMinimum(2)
        self.Count_spinBox.setMaximum(50)
        self.Count_spinBox.setObjectName("Count_spinBox")
        self.Speed_list = QtWidgets.QComboBox(self.centralwidget)
        self.Speed_list.setGeometry(QtCore.QRect(410, 540, 50, 50))
        self.Speed_list.addItems(["10", "100", "1000", "inf", "1"])
        self.Speed_list.setObjectName("Speed_list")
        self.Matrix_TextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.Matrix_TextEdit.setGeometry(QtCore.QRect(460, 540, 120, 50))
        self.Matrix_TextEdit.setObjectName("Matrix_TextEdit")
        self.Matrix_TextEdit.setText("[[1 1]\n [1 1]]")
        self.Import_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Import_btn.setGeometry(QtCore.QRect(580, 540, 120, 50))
        self.Import_btn.setObjectName("Import_btn")
        self.Random_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Random_btn.setGeometry(QtCore.QRect(700, 540, 90, 50))
        self.Random_btn.setObjectName("Random_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_functions()
        self.matrix = np.ones((2, 2)).astype(int)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Draw_btn.setText(_translate("MainWindow", "Draw"))
        self.Shake_btn.setText(_translate("MainWindow", "Move"))
        self.Clear_btn.setText(_translate("MainWindow", "One step"))
        self.Import_btn.setText(_translate("MainWindow", "Import JSON"))
        self.Random_btn.setText(_translate("MainWindow", "Random"))

    def add_functions(self):
        self.Draw_btn.clicked.connect(lambda: self.draw_random_nodes())
        self.Shake_btn.clicked.connect(lambda: self.move_nodes(self.Speed_list.currentText()))
        self.Clear_btn.clicked.connect(lambda: self.one_step())
        self.Count_spinBox.valueChanged.connect(lambda: self.set_matrix())
        self.Import_btn.clicked.connect(lambda: self.import_json('data/tree3_simple.json'))
        self.Random_btn.clicked.connect(lambda: self.random_graph())

    def check_symmetric(self):
        matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
        return np.allclose(matrix, matrix.T)

    def set_matrix(self):
        self.Matrix_TextEdit.setText(str(np.ones((self.Count_spinBox.value(), self.Count_spinBox.value())).astype(int)))

    def get_nodes(self):
        nodes = [item for item in self.scene.items() if isinstance(item, Node)]
        nodes.reverse()
        return nodes

    def get_edges(self):
        nodes = [item for item in self.scene.items() if isinstance(item, QGraphicsLineItem)]
        nodes.reverse()
        return nodes

    def get_nodes_coord(self):
        nodes = self.get_nodes()
        coord = list(map(get_coord, nodes))
        return np.array(coord)

    def draw_edge(self, x1, y1, x2, y2):
        line = QGraphicsLineItem(x1, y1, x2, y2)
        pen = QPen(Qt.blue)
        pen.setWidth(3)
        line.setPen(pen)
        self.scene.addItem(line)

    def draw_edges(self, coord_array=None):
        matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
        for edge in self.get_edges():
            self.scene.removeItem(edge)
        if coord_array is None:
            coord_array = self.get_nodes_coord()
        for i in range(len(coord_array)):
            for j in range(i, len(coord_array)):
                if i != j and matrix[i][j] == 1:
                    self.draw_edge(coord_array[i][0] + 30, coord_array[i][1] + 30,
                                   coord_array[j][0] + 30, coord_array[j][1] + 30)

    def draw_node(self, x, y, text):
        node = Node(0, 0, 50, 50, text, parent=self)
        node.setPos(x, y)
        node.setBrush(QBrush(Qt.red))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)

    def draw_nodes(self, coord_array):
        self.scene.clear()
        count = 0
        self.draw_edges(coord_array)
        for coord in coord_array:
            self.draw_node(coord[0], coord[1], str(count))
            count += 1

    def draw_random_nodes(self):
        if not self.check_symmetric():
            self.Matrix_TextEdit.setTextColor(Qt.red)
            self.Matrix_TextEdit.setText(self.Matrix_TextEdit.toPlainText())
        else:
            self.Matrix_TextEdit.setTextColor(Qt.black)
            self.Matrix_TextEdit.setText(self.Matrix_TextEdit.toPlainText())

            coord_array = []
            matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
            for i in range(matrix.shape[0]):
                x = random.randint(0, int(self.width - 50))
                y = random.randint(0, int(self.height - 50))
                coord_array.append([x, y])
            self.draw_nodes(np.array(coord_array))
            print(np.array(coord_array))
            print(self.check_symmetric())

    def distance(self):
        points = self.get_nodes_coord()
        length = len(points)
        distance = np.ones((length, length))
        for i in range(length):
            for j in range(length):
                distance[i][j] = np.linalg.norm(points[i] - points[j])
        return distance

    def attractive_forces(self, c):
        matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
        distance = self.distance()
        attractive = np.ones(distance.shape)
        l = c * np.sqrt(self.width * self.height / len(self.get_nodes()))
        for i in range(distance.shape[0]):
            for j in range(distance.shape[0]):
                attractive[i][j] = (distance[i][j] ** 2) / l
        return attractive * matrix

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

    def one_step(self):
        forces = np.sum(self.forces(1), axis=0)
        forces_sign = forces / np.absolute(forces)
        vectors = np.sum(self.unit_vectors(), axis=0) / len(self.get_nodes())

        old_coord = self.get_nodes_coord()
        new_coord = np.ones(old_coord.shape)

        for i in range(old_coord.shape[0]):
            new_coord[i] = old_coord[i] + (forces_sign[i] * vectors[i])

            if new_coord[i][0] <= 0 or new_coord[i][0] >= self.width - 50:
                new_coord[i][0] = old_coord[i][0]
            if new_coord[i][1] <= 0 or new_coord[i][1] >= self.height - 50:
                new_coord[i][1] = old_coord[i][1]

            if np.array_equal(new_coord[i], old_coord[i]):
                forces[i] = 0.0

        self.draw_nodes(new_coord)
        return forces

    def move_nodes(self, speed):
        while True:
            forces = self.one_step()
            if speed.isdigit():
                QtTest.QTest.qWait(int(100 ** (1 / int(speed))))
                print(abs(np.sum(forces)))
            # print(forces)
            # print(np.where(abs(forces) < 20)[0])
            # print(np.arange(len(forces)))

            # if np.array_equal(np.where(abs(forces) < 10)[0], np.arange(len(forces))):
            #     break
            if abs(np.sum(forces)) < 10:
                break

    def import_json(self, file_name):
        family_tree = FamilyTree(open_json(file_name))
        df = family_tree.get_links_pair_df()
        G = nx.from_pandas_edgelist(df, 'source_id', 'target_id')
        self.Matrix_TextEdit.setText(str(nx.adjacency_matrix(G).toarray()))
        # self.Count_spinBox.setValue(len(G.nodes()))

    def random_graph(self):
        matrix = np.random.randint(0, 2, size=(self.Count_spinBox.value(), self.Count_spinBox.value()))
        result = matrix
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0]):
                result[j][i] =matrix[i][j]
        self.Matrix_TextEdit.setText(str(result))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
