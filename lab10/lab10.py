from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
from math import sin
from horizon import float_horizon


red = Qt.red
blue = Qt.blue
black = Qt.black


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QGraphicsScene(0, 0, 711, 601)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.pen = QPen(black)
        draw_coord(self)
        self.draw.clicked.connect(lambda: draw(self))


def f(x, z):
    return sin(2 * x * z)


def draw_coord(win):
    win.scene.addLine(10, 10, 10, 591)
    win.scene.addLine(10, 10, 701, 10)


def draw(win):
    float_horizon(win.scene.width(), win.scene.height(), win.x_min.value(), win.x_max.value(), win.dx.value(),
            win.z_min.value(), win.z_max.value(), win.dz.value(), f, win.scene)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())