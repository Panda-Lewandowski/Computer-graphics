from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt
import math


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 711, 531)
        self.mainview.setScene(self.scene)
        self.pen = QPen()
        self.draw_line.clicked.connect(lambda: draw_line(self))
        self.clean_all.clicked.connect(self.scene.clear)
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_sun.clicked.connect(lambda: draw_sun(self))
        self.cda.setChecked(True)


def line_DDA(win, p1, p2):
    # Целочисленные значения координат начала и конца отрезка, округленные до ближайшего целого
    p11 = [int(p1[0]), int(p1[1])]
    p22= [int(p2[0]), int(p2[1])]

    # Длина и высота линии
    deltaX = abs(p11[0] - p22[0])
    deltaY = abs(p11[1] - p22[1])

    # Считаем минимальное количество итераций, необходимое для отрисовки отрезка.
    # Выбирая максимум из длины и высоты линии, обеспечиваем связность линии

    length = max(deltaX, deltaY)

    # особый случай, на экране закрашивается ровно один пиксел
    if length == 0:
        win.scene.addLine(p11[0], p11[1], p11[0] + 1, p11[1] + 1, win.pen)
        return

    # Вычисляем приращения на каждом шаге по осям абсцисс и ординат double
    dX = (p2[0] - p1[0]) / length
    dY = (p2[1] - p1[0]) / length

    # Начальные значения
    x = p1[0]
    y = p1[0]

    # Основной цикл
    while length:
        x += dX
        y += dY
        length -= 1
        win.scene.addLine(x, y, x+1, y+1, win.pen)


def line_br_float(win, p1, p2):
    deltax = abs(p2[0] - p1[0])
    deltay = abs(p2[1] - p1[0])
    error = 0
    deltaerr = deltay / deltax
    y = p1[1]
    for x in range(p1[0], p2[0]):
        print(x, y)
        win.scene.addLine(x, y, x + 1, y + 1, win.pen)
        error = error + deltaerr
        if error >= 0.5:
            y += 1
            error -= 1.0


def line_br_int(win, p1, p2):
    deltax = abs(p2[0] - p1[0])
    deltay = abs(p2[1] - p1[0])
    error = 0
    deltaerr = deltay
    y = p1[1]
    for x in range(p1[0], p2[0]):
        print(x, y)
        win.scene.addLine(x, y, x + 1, y + 1, win.pen)
        error = error + deltaerr
        if 2 * error >= deltax:
            y += 1
            error -= deltax

def draw_line(win):
    bx = win.begin_x.value()
    by = win.begin_y.value()
    ex = win.end_x.value()
    ey = win.end_y.value()

    if win.cda.isChecked():
        line_DDA(win, [bx, by], [ex, ey])
    if win.br_float.isChecked():
        line_br_float(win, [bx, by], [ex, ey])
    if win.br_int.isChecked():
        line_br_int(win, [bx, by], [ex, ey])
    if win.br_smooth.isChecked():
        pass
    if win.lib.isChecked():
        win.scene.addLine(bx, by, ex, ey, win.pen)


def draw_sun(win):
    d = win.spin_dia.value()
    spin = math.radians(win.spin_angle.value())
    t_x = 355
    t_y = 265
    bx = t_x
    by = t_y
    ex = bx + d
    ey = by
    """win.scene.addLine(bx, by, ex, ey, win.pen)
    teta = math.radians(spin)
    ex = t_x + (ex - t_x) * math.cos(teta) + (ey - t_y) * math.sin(teta)
    ey = t_y - (ex - t_x) * math.sin(teta) + (ey - t_y) * math.cos(teta)
    win.scene.addLine(bx, by, ex, ey, win.pen)"""

    """f win.cda.isChecked():
        teta = 0
        while teta <= 360:
            line_DDA(win, [bx, by], [ex, ey])
            bx = t_x + (bx - t_x) * math.cos(teta) + (by - t_y) * math.sin(teta)
            by = t_y - (bx - t_x) * math.sin(teta) + (by - t_y) * math.cos(teta)
            ex = t_x + (ex - t_x) * math.cos(teta) + (ey - t_y) * math.sin(teta)
            ey = t_y - (ex - t_x) * math.sin(teta) + (ey - t_y) * math.cos(teta)
            teta += spin"""

    if win.br_float.isChecked():
        pass
    if win.br_int.isChecked():
        pass
    if win.br_smooth.isChecked():
        pass
    if win.lib.isChecked():
        teta = spin
        print(teta)
        #while teta <= math.radians(360):
        win.scene.addLine(bx, by, ex, ey, win.pen)
        ex = t_x + (ex - t_x) * math.cos(teta) + (ey - t_y) * math.sin(teta)
        ey = t_y - (ex - t_x) * math.sin(teta) + (ey - t_y) * math.cos(teta)
        teta += spin
        print(teta)
        win.scene.addLine(bx, by, ex, ey, win.pen)


def get_color_bground(win):
    color = QtWidgets.QColorDialog.getColor(initial=QColor("ff00000"), title='Цвет фона',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        p = QPen()
        p.setColor(color)
        p.setWidth(100)
        s.addLine(0, 0, 10, 0, pen=p)
        win.bground_color.setScene(s)


def get_color_line(win):
    color = QtWidgets.QColorDialog.getColor(initial=QColor("ff00000"), title='Цвет фона',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        p = QPen()
        p.setColor(color)
        p.setWidth(100)
        s.addLine(0, 0, 10, 0, pen=p)
        win.line_color.setScene(s)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
