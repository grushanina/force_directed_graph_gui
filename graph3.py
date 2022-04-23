import math
import random
import warnings

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
    def __init__(self, x, y, w, h, text, parent, disp, c):
        super().__init__(x, y, w / c, h / c)
        self.font = QFont("Times", 20, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)
        self.parent = parent
        self.disp = disp
        self.c = c

    def mousePressEvent(self, event):
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(Node, self).mouseReleaseEvent(event)
        self.parent.draw_edges()

    def get_pos(self):
        return np.array([self.x(), self.y()])


class Edge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        self.v = node1
        self.u = node2
        pos1 = node1.get_pos()
        pos2 = node2.get_pos()
        super().__init__(pos1[0] + 30 / node1.c,
                         pos1[1] + 30 / node1.c,
                         pos2[0] + 30 / node2.c,
                         pos2[1] + 30 / node2.c)


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
        self.Mode_list = QtWidgets.QComboBox(self.centralwidget)
        self.Mode_list.setGeometry(QtCore.QRect(290, 540, 120, 50))
        self.Mode_list.addItems(["Full", "Line", "Circle", "Grid", "Tree", "Star", "Wheel"])
        self.Mode_list.setObjectName("Mode_list")
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
        self.Import_btn.setText(_translate("MainWindow", "Import JSON"))
        self.Random_btn.setText(_translate("MainWindow", "Random"))

    def add_functions(self):
        self.Draw_btn.clicked.connect(lambda: self.draw_random_nodes())
        self.Shake_btn.clicked.connect(lambda: self.move_nodes(self.Speed_list.currentText()))
        self.Count_spinBox.valueChanged.connect(lambda: self.set_matrix())
        self.Import_btn.clicked.connect(lambda: self.import_json('data/tree3_simple.json'))
        self.Random_btn.clicked.connect(lambda: self.random_graph())
        self.Mode_list.currentTextChanged.connect(lambda: self.set_mode())

    def check_symmetric(self):
        matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
        return np.allclose(matrix, matrix.T)

    def set_matrix(self):
        # self.Matrix_TextEdit.setText(str(np.ones((self.Count_spinBox.value(), self.Count_spinBox.value())).astype(int)))
        self.Matrix_TextEdit.setText(self.get_matrix_mode(self.Mode_list.currentText()))

    def get_nodes(self):
        nodes = [item for item in self.scene.items() if isinstance(item, Node)]
        nodes.reverse()
        return nodes

    def get_edges(self):
        edges = [item for item in self.scene.items() if isinstance(item, Edge)]
        edges.reverse()
        return edges

    def get_nodes_coord(self):
        nodes = self.get_nodes()
        coord = list(map(get_coord, nodes))
        return np.array(coord)

    def draw_edge(self, node1, node2):
        edge = Edge(node1, node2)
        pen = QPen(Qt.blue)
        pen.setWidth(3)
        edge.setPen(pen)
        self.scene.addItem(edge)

    def draw_edges(self):
        matrix = str_to_matrix(self.Matrix_TextEdit.toPlainText())
        for edge in self.get_edges():
            self.scene.removeItem(edge)
        nodes = self.get_nodes()
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                if i != j and matrix[i][j] == 1:
                    self.draw_edge(nodes[i], nodes[j])
                    # print(nodes[i], nodes[j])

    def draw_node(self, x, y, text):
        node = Node(0, 0, 50, 50, text,
                    parent=self,
                    disp=np.array([0, 0]),
                    c=1)
        node.setPos(x, y)
        node.setZValue(1)
        node.setBrush(QBrush(Qt.red))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)

    def draw_nodes(self, coord_array):
        self.scene.clear()
        count = 0
        for coord in coord_array:
            self.draw_node(coord[0], coord[1], str(count))
            count += 1
        self.draw_edges()

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

    def import_json(self, file_name):
        family_tree = FamilyTree(open_json(file_name))
        df = family_tree.get_links_pair_df()
        G = nx.from_pandas_edgelist(df, 'source_id', 'target_id')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.Matrix_TextEdit.setText(str(nx.adjacency_matrix(G).toarray()))
        # self.Count_spinBox.setValue(len(G.nodes()))

    def random_graph(self):
        matrix = np.random.randint(0, 2, size=(self.Count_spinBox.value(), self.Count_spinBox.value()))
        result = matrix
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[0]):
                result[j][i] = matrix[i][j]
        self.Matrix_TextEdit.setText(str(result))

    def f_a(self, x):
        k = np.sqrt(self.width * self.height / len(self.get_nodes())) / 5
        return x ** 2 / k

    def f_r(self, x):
        k = np.sqrt(self.width * self.height / len(self.get_nodes())) / 5
        return k ** 2 / x

    def one_step(self, vel):
        V = self.get_nodes()
        E = self.get_edges()
        # сила отталкивания
        for v in V:
            v.disp = np.array([0, 0])
            for u in V:
                if u != v:
                    delta = v.get_pos() - u.get_pos()
                    v.disp = v.disp + (delta / np.linalg.norm(delta)) * self.f_r(np.linalg.norm(delta))

        # сила притяжения
        for e in E:
            delta = e.v.get_pos() - e.u.get_pos()
            e.v.disp = e.v.disp - (delta / np.linalg.norm(delta)) * self.f_a(np.linalg.norm(delta))
            e.u.disp = e.u.disp + (delta / np.linalg.norm(delta)) * self.f_a(np.linalg.norm(delta))

        # перемещаем узлы
        for v in V:
            # вычисляем новые координаты
            new_pos = v.get_pos() + (v.disp / np.linalg.norm(v.disp)) * vel
            # огранение выхода узла за рамки
            new_pos[0] = min((self.width - 50), max(0, new_pos[0]))
            new_pos[1] = min((self.height - 50), max(0, new_pos[1]))
            # перемещаем
            v.setPos(new_pos[0], new_pos[1])

    def move_nodes(self, speed):
        vel = math.sqrt(self.width * self.height) * 0.1
        while vel > 0.1:
            if speed.isdigit():
                # QtTest.QTest.qWait(int(100 ** (1 / int(speed))))
                QtTest.QTest.qWait(int(speed))
            # QtTest.QTest.qWait(1)
            self.one_step(vel)
            self.draw_edges()
            vel *= 0.97
            print(vel)

    def set_mode(self):
        self.Matrix_TextEdit.setText(self.get_matrix_mode(self.Mode_list.currentText()))

    def get_matrix_mode(self, mode):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            edges = []
            n = self.Count_spinBox.value()

            if mode == 'Line':
                for i in range(n - 1):
                    edges.append((i, i + 1))

            if mode == 'Circle':
                edges = [(n - 1, 0)]
                for i in range(n - 1):
                    edges.append((i, i + 1))

            if mode == 'Grid':
                h = 3
                w = 3
                for i in range(h):
                    for j in range(w - 1):
                        u = i * w + j
                        v = u + 1
                        edges.append((u, v))
                for j in range(w):
                    for i in range(h - 1):
                        u = i * w + j
                        v = u + w
                        edges.append((u, v))

            if mode == 'Tree':
                for i in range(1, n):
                    j = (i - 1) // 2
                    edges.append((j, i))

            if mode == 'Star':
                for i in range(1, n):
                    edges.append((0, i))

            if mode == 'Wheel':
                for i in range(1, n):
                    edges.append((0, i))
                    j = i + 1 if i < n - 1 else 1
                    edges.append((i, j))

            if mode == 'Full':
                for i in range(n - 1):
                    for j in range(i + 1, n):
                        edges.append((i, j))

            G = nx.Graph(edges)
            return str(nx.adjacency_matrix(G).toarray())



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
