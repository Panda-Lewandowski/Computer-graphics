from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt
from math import sqrt, pi, cos, sin
import numpy as np
import time


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 511, 511)
        self.mainview.setScene(self.scene)
        self.image = QImage(511, 511, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.color_line = QColor(Qt.black)
        self.color_bground = QColor(Qt.white)
        self.draw_once.clicked.connect(lambda: draw_once(self))
        self.clean_all.clicked.connect(lambda: clear_all(self))
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_centr.clicked.connect(lambda: draw_centr(self))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.what)
        layout.addWidget(self.other)
        self.setLayout(layout)
        self.circle.setChecked(True)
        self.canon.setChecked(True)
        #self.circle.toggled.connect(lambda : change_text(self))

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def circle_canon(win, cx, cy, r):
    for x in range(0, r + 1, 1):
        y = int(sqrt(r ** 2 - x ** 2) + 0.5)
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def circle_param(win, cx, cy, r):
    l = int(pi * r / 2 + 0.5)  # длина четврети окружности
    for i in range(0, l + 1, 1):
        x = int(r * cos(i / r) + 0.5)
        y = int(r * sin(i / r) + 0.5)
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def circle_brez(win, cx, cy, r):
    x = 0
    y = r
    d = 2 - 2 * r
    b = 0
    while y >= 0:
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        if d < 0:  # пиксель лежит вне окружности
            b = 2 * d + 2 * y - 1
            x += 1

            if b <= 0:
                d = d + 2 * x + 1
            else:
                y -= 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d > 0:  # пиксель лежит внутри окружности
            b = 2 * d - 2 * x - 1
            y -= 1

            if b > 0:
                d = d - 2 * y + 1
            else:
                x += 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d == 0.0: # пиксель лежит на окружности
            x += 1
            y -= 1
            d = d + 2 * x - 2 * y + 2


def circle_middle(win, cx, cy, r):
    x = 0
    y = r
    p = 5 / 4 - r
    while True:
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())

        x += 1

        if p < 0:
            p += 2 * x + 1
        else:
            p += 2 * x - 2 * y + 5
            y -= 1

        if x > y:
            break


def ellips_canon(win, cx, cy, a, b):
    for x in range(0, a + 1, 1):
        y = int(b * sqrt(1.0 - x ** 2 / a / a) + 0.5)
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def ellips_param(win, cx, cy, a, b):
    m = max(a, b)
    l = int(pi * m / 2 + 0.5)
    for i in range(0, l + 1, 1):
        x = int(a * cos(i / m) + 0.5)
        y = int(b * sin(i / m) + 0.5)
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def ellips_brez(win, cx, cy, a, b):
    x = 0
    y = b
    a = a ** 2
    d = int(b ** 2 / 2 - a * b / 2 + a / 2 + 0.5)
    b = b ** 2
    while y >= 0:
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        if d < 0:  # пиксель лежит вне окружности
            beta = 2 * d + 2 * a * y - a
            x += 1
            if beta <= 0:
                d = d + 2 * b * x + b
            else:
                y -= 1
                d = d + 2 * b * x - 2 * a * y + a + b

            continue

        if d > 0:  # пиксель лежит внутри окружности
            beta = 2 * d - 2 * b * x - b
            y -= 1

            if beta > 0:
                d = d - 2 * y * a + a
            else:
                x += 1
                d = d + 2 * x * b - 2 * y * a + a + b

            continue

        if d == 0.0:  # пиксель лежит на окружности
            x += 1
            y -= 1
            d = d + 2 * x * b - 2 * y * a + a + b


def ellips_middle(win, cx, cy, a, b):
    x = 0
    y = b
    p = b * b - a * a * b + 0.25 * a * a
    while 2 * (b ** 2) * x < 2 * a * a * y:
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        x += 1

        if p < 0:
            p += 2 * b * b * x + b * b
        else:
            y -= 1
            p += 2 * b * b * x - 2 * a * a * y + b * b

    p = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b

    while y >= 0:
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        y -= 1

        if p > 0:
            p -= 2 * a * a * y + a * a
        else:
            x += 1
            p += 2 * b * b * x - 2 * a * a * y + a * a


def draw_once(win):
    is_standart = False
    #win.image.fill(win.color_bground) #TODO
    x = win.centr_x.value()
    y = win.centr_y.value()

    if win.circle.isChecked():
        r = win.rad.value()

        if win.canon.isChecked():
            circle_canon(win, x, y, r)
        if win.param.isChecked():
            circle_param(win, x, y, r)
        if win.brez.isChecked():
            circle_brez(win, x, y, r)
        if win.middle.isChecked():
            circle_middle(win, x, y, r)
        if win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - r, y - r, r * 2, r * 2, win.pen)

    if win.ellips.isChecked():
        a = win.a.value()
        b = win.b.value()

        if win.canon.isChecked():
            ellips_canon(win, x, y, b, a)
        if win.param.isChecked():
            ellips_param(win, x, y, b, a)
        if win.brez.isChecked():
            ellips_brez(win, x, y, b, a)
        if win.middle.isChecked():
            ellips_middle(win, x, y, b, a)
        if win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - b, y - a, b * 2, a * 2, win.pen)


    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


def draw_centr(win):
   # win.image.fill(win.color_bground)
    is_standart = False
    x = win.centr_x.value()
    y = win.centr_y.value()
    d = win.dia.value()
    c = win.count.value()


    if win.circle.isChecked():
        for i in range(d, d * c + d, d):

            if win.canon.isChecked():
                circle_canon(win, x, y, i)
            if win.param.isChecked():
                circle_param(win, x, y, i)
            if win.brez.isChecked():
                circle_brez(win, x, y, i)
            if win.middle.isChecked():
                circle_middle(win, x, y, i)
            if win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - i, y - i, i * 2, i * 2, win.pen)

    if win.ellips.isChecked():
        for i in range(d, d * c + d, d):
            if win.canon.isChecked():
                ellips_canon(win, x, y, i * 2, i)
            if win.param.isChecked():
                ellips_param(win, x, y, i * 2, i)
            if win.brez.isChecked():
                ellips_brez(win, x, y, i * 2, i)
            if win.middle.isChecked():
                ellips_middle(win, x, y, i * 2, i)
            if win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - i * 2, y - i, i * 4, i * 2, win.pen)


    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


def get_color_bground(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.white, title='Цвет фона',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_bground = color
        win.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.bground_color.setScene(s)
        win.scene.setBackgroundBrush(color)


def get_color_line(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.black, title='Цвет линии',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_line = color
        win.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.line_color.setScene(s)


def clear_all(win):
    win.image.fill(Qt.color0)
    win.scene.clear()


def change_text(win):
    if win.circle.isChecked():
        win.draw_once.setText('lolloolol')
    if win.ellips.isChecked():
        win.draw_onсe.setText('aaaaaaaaaa')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
