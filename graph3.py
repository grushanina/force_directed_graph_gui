import math
import os.path
import random
import sys
import time
import warnings

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtTest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QColor, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem, \
    QGraphicsRectItem, QSizePolicy, QLayout

from FamilyTree import *

np.set_printoptions(threshold=sys.maxsize)


def str_to_matrix(string):
    result = []
    matrix_string = string[1:-1]
    for row in matrix_string.split('\n '):
        cur_row = np.array(row[1:-1].split(' ')).astype(int)
        result.append(cur_row)
    return np.array(result)


def get_coord(point):
    return np.array([point.x(), point.y()])


class NodeFemale(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, text, parent, disp, node_id):
        super().__init__(x, y, w, h)
        self.font = QFont("Times", 15, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)
        self.parent = parent
        self.disp = disp
        self.size = w
        self.node_id = node_id

    def mousePressEvent(self, event):
        image = QPixmap('img/no_avatar.jpg')
        if self.parent.family_tree[self.node_id]['type'] == 'person':
            self.parent.Name_label.setText(self.parent.family_tree[self.node_id]['name'])
            self.parent.Age_label.setText(self.parent.family_tree[self.node_id]['date'])
            if os.path.isfile('img/' + str(self.node_id) + '.jpg'):
                image = QPixmap('img/' + str(self.node_id) + '.jpg')
            children = 'Дети:\n'
            for child_id in self.parent.family_tree[self.node_id]['cids']:
                children += self.parent.family_tree[child_id]['name'] + '\n'
            self.parent.Children_label.setText(children)
            print(children)

        if self.parent.family_tree[self.node_id]['type'] == 'family':
            self.parent.Name_label.setText("Имя")
            self.parent.Age_label.setText("Возраст")
            self.parent.Children_label.setText("Дети")
        image = image.scaledToWidth(269)
        image = image.scaledToHeight(269)
        self.parent.Img_label.setPixmap(image)

        for node in self.parent.get_nodes():
            node.setPen(QPen(Qt.black, 1))
        self.setPen(QPen(Qt.black, 3))

        for node in self.parent.get_nodes():
            if self.parent.family_tree[self.node_id]['type'] == 'person':
                if node.node_id == self.parent.family_tree[self.node_id]['id']:
                    if self.parent.family_tree[self.node_id]['gender'] == 'female':
                        color = QColor(255, 148, 217, 255)
                    else:
                        color = QColor(148, 217, 255, 255)
                    node.setBrush(QBrush(color))
                elif node.node_id in self.parent.family_tree[self.node_id]['pids']:
                    node.setBrush(QBrush(QColor(240, 21, 111, 255)))
                elif node.node_id in self.parent.family_tree[self.node_id]['cids']:
                    node.setBrush(QBrush(QColor(77, 240, 184, 255)))
                else:
                    node.setBrush(QBrush(Qt.gray))

                if 'mid' in self.parent.family_tree[self.node_id].keys():
                    if node.node_id == self.parent.family_tree[self.node_id]['mid']:
                        node.setBrush(QBrush(QColor(64, 117, 240, 255)))
                if 'fid' in self.parent.family_tree[self.node_id].keys():
                    if node.node_id == self.parent.family_tree[self.node_id]['fid']:
                        node.setBrush(QBrush(QColor(64, 117, 240, 255)))

        super(NodeFemale, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(NodeFemale, self).mouseReleaseEvent(event)
        self.parent.draw_edges()
        print(self.x())
        print(self.y())

    def get_pos(self):
        return np.array([self.x(), self.y()])


class NodeMale(QGraphicsRectItem):
    def __init__(self, x, y, w, h, text, parent, disp, node_id):
        super().__init__(x, y, w, h)
        self.font = QFont("Times", 15, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)
        self.parent = parent
        self.disp = disp
        self.size = w
        self.node_id = node_id

    def mousePressEvent(self, event):
        image = QPixmap('img/no_avatar.jpg')
        if self.parent.family_tree[self.node_id]['type'] == 'person':
            self.parent.Name_label.setText(self.parent.family_tree[self.node_id]['name'])
            self.parent.Age_label.setText(self.parent.family_tree[self.node_id]['date'])
            if os.path.isfile('img/' + str(self.node_id) + '.jpg'):
                image = QPixmap('img/' + str(self.node_id) + '.jpg')
            children = 'Дети:\n'
            for child_id in self.parent.family_tree[self.node_id]['cids']:
                children += self.parent.family_tree[child_id]['name'] + '\n'
            self.parent.Children_label.setText(children)
            print(children)

        if self.parent.family_tree[self.node_id]['type'] == 'family':
            self.parent.Name_label.setText("Имя")
            self.parent.Age_label.setText("Возраст")
            self.parent.Children_label.setText("Дети")
        image = image.scaledToWidth(269)
        image = image.scaledToHeight(269)
        self.parent.Img_label.setPixmap(image)

        for node in self.parent.get_nodes():
            node.setPen(QPen(Qt.black, 1))
        self.setPen(QPen(Qt.black, 3))

        for node in self.parent.get_nodes():
            if self.parent.family_tree[self.node_id]['type'] == 'person':
                if node.node_id == self.parent.family_tree[self.node_id]['id']:
                    if self.parent.family_tree[self.node_id]['gender'] == 'female':
                        color = QColor(255, 148, 217, 255)
                    else:
                        color = QColor(148, 217, 255, 255)
                    node.setBrush(QBrush(color))
                elif node.node_id in self.parent.family_tree[self.node_id]['pids']:
                    node.setBrush(QBrush(QColor(240, 21, 111, 255)))
                elif node.node_id in self.parent.family_tree[self.node_id]['cids']:
                    node.setBrush(QBrush(QColor(77, 240, 184, 255)))
                else:
                    node.setBrush(QBrush(Qt.gray))

                if 'mid' in self.parent.family_tree[self.node_id].keys():
                    if node.node_id == self.parent.family_tree[self.node_id]['mid']:
                        node.setBrush(QBrush(QColor(64, 117, 240, 255)))
                if 'fid' in self.parent.family_tree[self.node_id].keys():
                    if node.node_id == self.parent.family_tree[self.node_id]['fid']:
                        node.setBrush(QBrush(QColor(64, 117, 240, 255)))

        super(NodeMale, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(NodeMale, self).mouseReleaseEvent(event)
        self.parent.draw_edges()
        print(self.x())
        print(self.y())

    def get_pos(self):
        return np.array([self.x(), self.y()])


class Edge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        self.v = node1
        self.u = node2
        pos1 = node1.get_pos()
        pos2 = node2.get_pos()
        super().__init__(pos1[0] + node1.size / 2,
                         pos1[1] + node1.size / 2,
                         pos2[0] + node2.size / 2,
                         pos2[1] + node2.size / 2)


class Graph_view(QtWidgets.QGraphicsView):
    def __init__(self, parent, main):
        super(Graph_view, self).__init__(parent)
        self._zoom = 0
        self.main = main

    def wheelEvent(self, event):
        print(self.main.width)
        print(self.main.height)

        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        if self._zoom > 0:
            self.scale(factor, factor)
        else:
            self.scale(factor, factor)

        self.main.width = self.main.width / factor
        self.main.height = self.main.height / factor


class Legend(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)


class TimeText(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Draw_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Draw_btn.setGeometry(QtCore.QRect(50, 740, 120, 50))
        self.Draw_btn.setObjectName("Draw_btn")
        self.graphicsView = Graph_view(self.centralwidget, self)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1200, 740))
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, 1198.0, 738.0))
        self.graphicsView.setObjectName("graphicsView")
        self.width_base = 1198.0
        self.height_base = 738.0
        self.width = 1198.0
        self.height = 738.0
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, self.width, self.height))
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.Shake_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Shake_btn.setGeometry(QtCore.QRect(170, 740, 120, 50))
        self.Shake_btn.setObjectName("Shake_btn")
        self.Mode_list = QtWidgets.QComboBox(self.centralwidget)
        self.Mode_list.setGeometry(QtCore.QRect(290, 740, 60, 50))
        self.Mode_list.addItems(["Full", "Line", "Circle", "Grid", "Tree", "Star", "Wheel"])
        self.Mode_list.setObjectName("Mode_list")
        self.K_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.K_spinBox.setGeometry(QtCore.QRect(350, 740, 60, 50))
        self.K_spinBox.setObjectName("K_spinBox")
        self.K_spinBox.setMinimum(1)
        self.K_spinBox.setMaximum(20)
        self.Count_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.Count_spinBox.setGeometry(QtCore.QRect(0, 740, 50, 50))
        self.Count_spinBox.setMinimum(2)
        self.Count_spinBox.setMaximum(100)
        self.Count_spinBox.setObjectName("Count_spinBox")
        self.Speed_list = QtWidgets.QComboBox(self.centralwidget)
        self.Speed_list.setGeometry(QtCore.QRect(410, 740, 50, 50))
        self.Speed_list.addItems(["10", "100", "1000", "inf", "1"])
        self.Speed_list.setObjectName("Speed_list")
        self.Matrix_TextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.Matrix_TextEdit.setGeometry(QtCore.QRect(460, 740, 120, 50))
        self.Matrix_TextEdit.setObjectName("Matrix_TextEdit")
        self.Matrix_TextEdit.setText("[[1 1]\n [1 1]]")
        self.Import_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Import_btn.setGeometry(QtCore.QRect(580, 740, 65, 50))
        self.Import_btn.setObjectName("Import_btn")
        self.Export_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Export_btn.setGeometry(QtCore.QRect(645, 740, 65, 50))
        self.Export_btn.setObjectName("Export_btn")
        self.Json_line = QtWidgets.QLineEdit(self.centralwidget)
        self.Json_line.setGeometry(QtCore.QRect(710, 740, 90, 50))
        self.Json_line.setObjectName("Json_line")
        self.Save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Save_btn.setGeometry(QtCore.QRect(800, 740, 65, 50))
        self.Save_btn.setObjectName("Save_btn")
        self.Legend_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Legend_btn.setGeometry(QtCore.QRect(865, 740, 65, 50))
        self.Legend_btn.setObjectName("Legend_btn")
        self.Time_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Time_btn.setGeometry(QtCore.QRect(930, 740, 65, 50))
        self.Time_btn.setObjectName("Time_btn")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1210, 290, 271, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.Name_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Name_label.setFont(font)
        self.Name_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Name_label.setObjectName("Name_label")
        self.Name_label.setWordWrap(True)
        self.verticalLayout.addWidget(self.Name_label)
        self.Age_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Age_label.setFont(font)
        self.Age_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Age_label.setObjectName("Age_label")
        self.Age_label.setWordWrap(True)
        self.verticalLayout.addWidget(self.Age_label)
        self.Children_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Children_label.setFont(font)
        self.Children_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Children_label.setObjectName("Children_label")
        self.Children_label.setWordWrap(True)
        self.Children_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.verticalLayout.addWidget(self.Children_label)
        self.Img_label = QtWidgets.QLabel(self.centralwidget)
        self.Img_label.setGeometry(QtCore.QRect(1210, 0, 269, 269))
        self.Img_label.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.Img_label.setFont(font)
        self.Img_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Img_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Img_label.setText("")
        self.Img_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Img_label.setObjectName("Img_label")
        self.Image = QPixmap('img/no_avatar.jpg')
        self.Image = self.Image.scaledToWidth(269)
        self.Image = self.Image.scaledToHeight(269)
        self.Img_label.setPixmap(self.Image)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_functions()
        self.matrix = np.ones((2, 2)).astype(int)
        self.family_tree = {0: {'type': 'node', 'shortname': '0', 'gender': 'female'},
                            1: {'type': 'node', 'shortname': '1', 'gender': 'female'}}
        self.legend_on = False
        self.time_on = False
        self.result_time = 0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Draw_btn.setText(_translate("MainWindow", "Draw"))
        self.Shake_btn.setText(_translate("MainWindow", "Move"))
        self.Import_btn.setText(_translate("MainWindow", "Import"))
        self.Export_btn.setText(_translate("MainWindow", "Export"))
        self.Json_line.setText(_translate("MainWindow", "tree3_simple"))
        self.Save_btn.setText(_translate("MainWindow", "Save"))
        self.Legend_btn.setText(_translate("MainWindow", "Legend"))
        self.Time_btn.setText(_translate("MainWindow", "Time"))
        self.Name_label.setText(_translate("MainWindow", "Имя"))
        self.Age_label.setText(_translate("MainWindow", "Возраст"))
        self.Children_label.setText(_translate("MainWindow", "Дети"))

    def add_functions(self):
        self.Draw_btn.clicked.connect(lambda: self.draw_random_nodes())
        self.Shake_btn.clicked.connect(lambda: self.move_nodes(self.Speed_list.currentText()))
        self.Count_spinBox.valueChanged.connect(lambda: self.set_matrix())
        self.Import_btn.clicked.connect(lambda: self.import_json('data/' + self.Json_line.text() + '.json'))
        self.Mode_list.currentTextChanged.connect(lambda: self.set_mode())
        self.Export_btn.clicked.connect(lambda: self.export_json())
        self.Save_btn.clicked.connect(lambda: self.save_img())
        self.Legend_btn.clicked.connect(lambda: self.show_legend())
        self.Time_btn.clicked.connect(lambda: self.show_time())

    def check_symmetric(self):
        return np.allclose(self.matrix, self.matrix.T)

    def set_matrix(self):
        # self.Matrix_TextEdit.setText(str(np.ones((self.Count_spinBox.value(), self.Count_spinBox.value())).astype(int)))
        self.Matrix_TextEdit.setText(str(self.get_matrix_mode(self.Mode_list.currentText())))
        self.matrix = self.get_matrix_mode(self.Mode_list.currentText())
        self.family_tree = {}
        for i in range(self.matrix.shape[0]):
            self.family_tree.update({i: {'type': 'node', 'shortname': str(i), 'gender': 'female'}})
        print(self.family_tree)

    def get_nodes(self):
        nodes = [item for item in self.scene.items() if isinstance(item, NodeFemale) or isinstance(item, NodeMale)]
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
        pen = QPen(Qt.black)
        pen.setWidth(3)
        edge.setPen(pen)
        self.scene.addItem(edge)

    def draw_edges(self):
        for edge in self.get_edges():
            self.scene.removeItem(edge)
        nodes = self.get_nodes()
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                if i != j and self.matrix[i][j] == 1:
                    self.draw_edge(nodes[i], nodes[j])

    def draw_node(self, x, y, size, text, color, node_id, gender):
        if gender == 'female':
            node = NodeFemale(0, 0, size, size, text,
                              parent=self,
                              disp=np.array([0, 0]),
                              node_id=node_id)
        else:
            node = NodeMale(0, 0, size, size, text,
                            parent=self,
                            disp=np.array([0, 0]),
                            node_id=node_id)
        node.setPos(x, y)
        node.setZValue(1)
        node.setBrush(QBrush(color))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)

    def draw_nodes(self, coord_array):
        self.scene.clear()
        count = 0
        for node_id in self.family_tree:
            size = 5
            text = ''
            color = QColor(0, 0, 0, 255)
            x = coord_array[count][0]
            y = coord_array[count][1]
            gender = 'female'
            if self.family_tree[node_id]['type'] != 'family':
                size = 40
                text = self.family_tree[node_id]['shortname']
                if self.family_tree[node_id]['gender'] == 'female':
                    color = QColor(255, 148, 217, 255)
                    gender = 'female'
                else:
                    color = QColor(148, 217, 255, 255)
                    gender = 'male'
            if self.family_tree[node_id]['type'] != 'node':
                if 'x' in self.family_tree[node_id].keys():
                    x = self.family_tree[node_id]['x']
                if 'y' in self.family_tree[node_id].keys():
                    y = self.family_tree[node_id]['y']
            self.draw_node(x, y, size, text, color, node_id, gender)
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
            left = -(self.width - self.width_base) / 2
            right = self.width + (self.width_base - self.width) / 2 - 40
            top = -(self.height - self.height_base) / 2
            bottom = self.height + (self.height_base - self.height) / 2 - 40
            for i in range(self.matrix.shape[0]):
                # x = random.randint(0, int(self.width - 50))
                # y = random.randint(0, int(self.height - 50))
                x = random.randint(int(left), int(right))
                y = random.randint(int(top), int(bottom))
                coord_array.append([x, y])
            self.draw_nodes(np.array(coord_array))

    def import_json(self, file_name):
        if os.path.isfile(file_name):
            family_tree = FamilyTree(open_json(file_name))
            G = family_tree.get_networkx_graph()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.Matrix_TextEdit.setText(str(nx.adjacency_matrix(G).toarray()))
                self.matrix = nx.adjacency_matrix(G).toarray()
            self.family_tree = dict(family_tree.get_networkx_graph().nodes(data=True))
            print(self.family_tree)
        else:
            self.Json_line.setText('No file')

    def f_a(self, x):
        k = np.sqrt(self.width * self.height / len(self.get_nodes())) / int(self.K_spinBox.value())
        return x ** 2 / k

    def f_r(self, x):
        k = np.sqrt(self.width * self.height / len(self.get_nodes())) / int(self.K_spinBox.value())
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
            left = -(self.width - self.width_base) / 2
            right = self.width + (self.width_base - self.width) / 2 - 40
            top = -(self.height - self.height_base) / 2
            bottom = self.height + (self.height_base - self.height) / 2 - 40
            new_pos[0] = min(right, max(left, new_pos[0]))
            new_pos[1] = min(bottom, max(top, new_pos[1]))
            # перемещаем
            v.setPos(new_pos[0], new_pos[1])

    def move_nodes(self, speed):
        vel = math.sqrt(self.width * self.height) * 0.1
        start_time = time.time()
        while vel > 0.1:
            if speed.isdigit():
                QtTest.QTest.qWait(int(speed))
            self.one_step(vel)
            self.draw_edges()
            vel *= 0.975
            print(vel)
        result_time = time.time() - start_time
        print("--- %s seconds ---" % round(result_time, 4))
        self.result_time = round(result_time, 4)

    def set_mode(self):
        self.Matrix_TextEdit.setText(str(self.get_matrix_mode(self.Mode_list.currentText())))
        self.matrix = self.get_matrix_mode(self.Mode_list.currentText())

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
                h = 5
                w = 5
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
            return nx.adjacency_matrix(G).toarray()

    def export_json(self):
        result = []
        tree = self.family_tree
        for node in self.get_nodes():
            tree[node.node_id].update({'x': node.pos().x()})
            tree[node.node_id].update({'y': node.pos().y()})

        for node_id in tree:
            result.append(tree[node_id])

        with open("data/sample.json", "w") as outfile:
            json.dump(result, outfile)
        with open("data/sample.json", "r") as outfile:
            out = outfile.read().replace('[{', '[\n {').replace('}]', '}\n]').replace('},', '},\n')
        with open("data/sample.json", "w") as outfile:
            outfile.write(out)

    def save_img(self):
        area = self.scene.sceneRect()
        image = QImage(area.width(), area.height(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
        self.scene.render(painter, QtCore.QRectF(image.rect()), area)
        painter.end()
        image.save("capture.png")
        print('Image saved!')

    def show_legend(self):
        if not self.legend_on:
            for item in self.scene.items():
                if isinstance(item, Legend):
                    item.setVisible(True)
                    self.legend_on = True
                    self.Legend_btn.setStyleSheet("background-color: DarkGrey")
                    return

            legend = Legend(0, 0, 100, 80)
            legend.setPos(5, 5)
            legend.setZValue(2)
            legend.setPen(QPen(Qt.black, 1))
            legend.setFlag(QGraphicsItem.ItemIsMovable)

            parents_box = QGraphicsRectItem(5, 5, 20, 20, parent=legend)
            parents_box.setBrush(QBrush(QColor(64, 117, 240, 255)))
            parents_text = QGraphicsTextItem('- родители', parent=legend)
            parents_text.setFont(QFont("Times", 8, QFont.Bold))
            parents_text.setPos(30, 5)

            spouses_box = QGraphicsRectItem(5, 30, 20, 20, parent=legend)
            spouses_box.setBrush(QBrush(QColor(240, 21, 111, 255)))
            parents_text = QGraphicsTextItem('- супруги', parent=legend)
            parents_text.setFont(QFont("Times", 8, QFont.Bold))
            parents_text.setPos(30, 30)

            children_box = QGraphicsRectItem(5, 55, 20, 20, parent=legend)
            children_box.setBrush(QBrush(QColor(77, 240, 184, 255)))
            parents_text = QGraphicsTextItem('- дети', parent=legend)
            parents_text.setFont(QFont("Times", 8, QFont.Bold))
            parents_text.setPos(30, 55)

            self.scene.addItem(legend)
            self.legend_on = True
            self.Legend_btn.setStyleSheet("background-color: DarkGrey")
        else:
            for item in self.scene.items():
                if isinstance(item, Legend):
                    item.setVisible(False)
            self.legend_on = False
            self.Legend_btn.setStyleSheet("background-color: light gray")

    def show_time(self):
        if not self.time_on:
            for item in self.scene.items():
                if isinstance(item, TimeText):
                    item.setVisible(True)
                    self.time_on = True
                    self.Time_btn.setStyleSheet("background-color: DarkGrey")
                    item.setPlainText(str(self.result_time) + ' с.')
                    return

            time_text = TimeText(str(self.result_time) + ' с.')
            time_text.setFont(QFont("Times", 8, QFont.Bold))
            time_text.setPos(1100.0, 700.0)
            time_text.setZValue(2)
            time_text.setFlag(QGraphicsItem.ItemIsMovable)
            self.scene.addItem(time_text)
            self.time_on= True
            self.Time_btn.setStyleSheet("background-color: DarkGrey")
        else:
            for item in self.scene.items():
                if isinstance(item, TimeText):
                    item.setVisible(False)
            self.time_on = False
            self.Time_btn.setStyleSheet("background-color: light gray")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
