from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen, QImage, QPixmap
from PyQt5.QtCore import Qt
from math import sin, cos
from horizon import float_horizon


red = Qt.red
blue = Qt.blue
black = Qt.black
white = Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QGraphicsScene(0, 0, 711, 601)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(710, 600, QImage.Format_Alpha8)
        self.image.fill(black)
        self.pen = QPen(black)
        self.draw.clicked.connect(lambda: draw(self))
        self.dial_x.valueChanged.connect(lambda: draw(self))
        self.dial_y.valueChanged.connect(lambda: draw(self))
        self.dial_z.valueChanged.connect(lambda: draw(self))


def f(x, z):
    return cos(x) * sin(z)


def draw(win):
    win.scene.clear()
    win.image.fill(black)
    tx = win.dial_x.value()
    ty = win.dial_y.value()
    tz = win.dial_z.value()

    win.image = float_horizon(win.scene.width(), win.scene.height(), win.x_min.value(), win.x_max.value(), win.dx.value(),
            win.z_min.value(), win.z_max.value(), win.dz.value(), tx, ty, tz, f, win.image)

    pix = QPixmap()
    pix.convertFromImage(win.image)
    win.scene.addPixmap(pix)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())