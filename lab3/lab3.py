from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt
from math import cos, sin, pi, radians, copysign
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
        self.color_line = QColor()
        self.color_bground = QColor()
        self.draw_line.clicked.connect(lambda: draw_line(self))
        self.clean_all.clicked.connect(lambda : clear_all(self))
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_sun.clicked.connect(lambda: draw_sun(self))
        self.cda.setChecked(True)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def line_DDA(win, p1, p2):
    # Длина и высота линии
    deltaX = abs(p1[0] - p2[0])
    deltaY = abs(p1[1] - p2[1])

    # Считаем минимальное количество итераций, необходимое для отрисовки отрезка.
    # Выбирая максимум из длины и высоты линии, обеспечиваем связность линии

    length = max(deltaX, deltaY)

    # особый случай, на экране закрашивается ровно один пиксел
    if length == 0:
        win.image.setPixel(p1[0], p1[1], win.pen.color().rgb())
        return

    # Вычисляем приращения на каждом шаге по осям абсцисс и ординат double
    dX = (p2[0] - p1[0]) / length
    dY = (p2[1] - p1[0]) / length

    # Начальные значения
    x = p1[0] + 0.5 * sign(dX)
    y = p1[1] + 0.5 * sign(dY)

    # Основной цикл
    while length > 0:
        win.image.setPixel(x, y, win.pen.color().rgb())
        x += dX
        y += dY
        length -= 1


def line_br_float(win, p1, p2):
    if p1 == p2:
        win.image.setPixel(p1[0], p1[1], win.pen.color().rgb())
        return
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[0]
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    x = p1[0]
    y = p1[1]

    change = False

    if dy > dx:
        temp = dx
        dx = dy
        dy = temp
        change = True

    try:
        h = dy / dx
    except ZeroDivisionError:
        return

    e = h - 0.5
    i = 1
    while i <= dx:
        win.image.setPixel(x, y, win.pen.color().rgb())
        if e >= 0:
            if change is False:
                y += sy
            else:
                x += sx
            e -= 1

        if e < 0:
            if change is False:
                x += sx
            else:
                y += sy
            e += h
        i+=1


def line_br_int(win, p1, p2):
    if p1 == p2:
        win.image.setPixel(p1[0], p1[1], win.pen.color().rgb())
        return
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[0]
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    x = p1[0]
    y = p1[1]

    change = False

    if dy > dx:
        temp = dx
        dx = dy
        dy = temp
        change = True

    e = 2 * dy - dx
    i = 1
    while i <= dx:
        win.image.setPixel(x, y, win.pen.color().rgb())
        if e >= 0:
            if change == 0:
                y += sy
            else:
                x += sx
            e -= 2 * dx

        if e < 0:
            if change == 0:
                x += sx
            else:
                y += sy
            e += (2 * dy)
        i += 1


def line_br_smooth(win, p1, p2):
    if p1 == p2:
        win.image.setPixel(p1[0], p1[1], win.pen.color().rgb())
        return

    win.pen.setColor(win.color_line)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[0]
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    x = p1[0]
    y = p1[1]

    try:
        h = dy / dx
    except ZeroDivisionError:
        h = 0.1


    isBlack = False

    if win.pen.color() == Qt.black:
        i_max = 256
        isBlack = True
    else:
        i_max = 100

    change = False

    if dy > dx:
        temp = dx
        dx = dy
        dy = temp
        change = True
        h = 1 / h

    h *= i_max
    e = i_max/2
    w = i_max - h
    i = 1
    while i <= dx:
        if not isBlack:
            win.pen.setColor(win.pen.color().lighter(100 + e))
            win.image.setPixel(x, y, win.pen.color().rgba())
        else:
            new = QColor()
            new.setRgb(0, 0, 0, alpha=255 - e)
            win.pen.setColor(new)
            win.image.setPixel(x, y, win.pen.color().rgba())
        if e <= w:
            if change:
                y += sy
            else:
                x += sx
            e += h
        else:
            x += sx
            y += sy
            e -= w
        i += 1


def line_draw_Wu(win, p1, p2):
    pass


def draw_line(win):
    bx = win.begin_x.value()
    by = win.begin_y.value()
    ex = win.end_x.value()
    ey = win.end_y.value()
    is_standart =False
    win.image.fill(win.color_bground)
    if win.cda.isChecked():
        start = time.clock()
        line_DDA(win, [bx, by], [ex, ey])
        end = time.clock()
    if win.br_float.isChecked():
        start = time.clock()
        line_br_float(win, [bx, by], [ex, ey])
        end = time.clock()
    if win.br_int.isChecked():
        start = time.clock()
        line_br_int(win, [bx, by], [ex, ey])
        end = time.clock()
    if win.br_smooth.isChecked():
        start = time.clock()
        line_br_smooth(win, [bx, by], [ex, ey])
        end = time.clock()
    if win.lib.isChecked():
        is_standart = True
        start = time.clock()
        win.scene.addLine(bx, by, ex, ey, win.pen)
        end = time.clock()

    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)

    win.label.setText("{0:.3f}msc".format((end - start)*1000))


def draw_sun(win):
    d = win.spin_dia.value()
    spin = win.spin_angle.value()
    bx = 255
    by = 255
    win.image.fill(win.color_bground)
    is_standart = False
    for i in np.arange(0, 360, spin):
        ex = cos(radians(i)) * d + 255
        ey = sin(radians(i)) * d + 255

        if win.cda.isChecked():
            start = time.clock()
            line_DDA(win, [bx, by], [ex, ey])
            end = time.clock()
        if win.br_float.isChecked():
            start = time.clock()
            line_br_float(win, [bx, by], [ex, ey])
            end = time.clock()
        if win.br_int.isChecked():
            start = time.clock()
            line_br_int(win, [bx, by], [ex, ey])
            end = time.clock()
        if win.br_smooth.isChecked():
            start = time.clock()
            line_br_smooth(win, [bx, by], [ex, ey])
            end = time.clock()
        if win.lib.isChecked():
            is_standart = True
            start = time.clock()
            win.scene.addLine(bx, by, ex, ey, win.pen)
            end = time.clock()

    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)

    win.label.setText("{0:.3f}msc".format((end - start) * 1000))


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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
