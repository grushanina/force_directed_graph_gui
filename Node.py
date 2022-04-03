from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem


class Node(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h)
        self.font = QFont("Times", 20, QFont.Bold)
        self.text = QGraphicsTextItem(text, parent=self)
        self.text.setFont(self.font)
        self.text.setPos(x, y)

    def mousePressEvent(self, event):
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(Node, self).mouseReleaseEvent(event)

    def get_pos(self):
        return self.x(), self.y()