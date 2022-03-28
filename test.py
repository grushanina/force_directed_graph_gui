from PyQt5 import QtCore, QtGui, QtWidgets
import random

from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import Qt


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        self.ellipse_item = self.addEllipse(0, 0, 50, 50, brush=QBrush(Qt.red))
        self.ellipse_item.setPos(50, 50)


    def mousePressEvent(self, event):
        items = self.items(event.scenePos())
        for item in items:
            if item is self.ellipse_item:
                print(item.mapFromScene(event.scenePos()))
        super(Scene, self).mousePressEvent(event)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    scene = Scene()
    w = QtWidgets.QGraphicsView(scene)
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())