# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, \
    QGraphicsSceneDragDropEvent, QGraphicsSceneHoverEvent
from PyQt5.QtCore import Qt, QPointF
import random


class Field(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, field, parent):
        super().__init__(x - field/2, y - field/2, w + field, h + field, parent=parent)
        self.parent = parent

    def get_parent(self):
        return self.parent

class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, field):
        super().__init__(x, y, w, h)
        self.field = Field(x, y, w, h, field=field, parent=self)


    def mousePressEvent(self, event):
        print('Press')
        super(Node, self).mousePressEvent(event)



    def mouseReleaseEvent(self, event):
        print('Release')
        # print(list(set(self.field.collidingItems()).difference({self})))
        # print(list(map(type, self.field.collidingItems())))
        colliding = [x for x in self.field.collidingItems() if not isinstance(x, Node)]
        colliding_points = list(map(Field.get_parent, colliding))
        colliding_points_pos = list(map(Node.get_pos, colliding_points))
        print(colliding_points_pos)
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
        self.graphicsView.setSceneRect(QtCore.QRectF(0.0, 0.0, 798.0, 538.0))

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
        self.Draw_btn.clicked.connect(lambda: self.draw_node())
        self.Clear_btn.clicked.connect(lambda: self.clear())

    def draw_rect(self):
        rect = QGraphicsRectItem(0, 0, 200, 50)
        rect.setPos(50, 20)
        brush = QBrush(Qt.red)
        rect.setBrush(brush)
        pen = QPen(Qt.cyan)
        pen.setWidth(10)
        rect.setPen(pen)
        self.scene.addItem(rect)
        print(self.scene.items()[0].x())

    def draw_ellipse(self, x, y):
        ellipse = QGraphicsEllipseItem(0, 0, 50, 50)
        ellipse.setPos(x, y)
        ellipse.setBrush(QBrush(Qt.red))
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(ellipse)

    def draw_ellipses(self):
        for i in range(self.Count_spinBox.value()):
            x = random.randint(0, 748)
            y = random.randint(0, 488)
            self.draw_ellipse(x, y)
            print(list(map(QGraphicsItem.x, self.scene.items())))

    def clear(self):
        self.scene.clear()

    def draw_node(self):
        node = Node(0, 0, 50, 50, 50)
        node.setPos(50, 50)
        node.setBrush(QBrush(Qt.red))
        node.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(node)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
