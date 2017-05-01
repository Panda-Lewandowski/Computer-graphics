from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
import time

col_one = QColor(0, 0, 0)
col_zero = QColor(255, 255, 255)
point_zat = False
circle = False

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = myScene(0, 0, 561, 581)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(col_zero)
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: fill_with_seed(self))
        self.addpoint.clicked.connect(lambda: add_point_by_btn(self))
        self.pixel.clicked.connect(lambda: set_flag_zat(self))
        self.addcircle.clicked.connect(lambda: set_flag_cir(self))
        self.edges = []
        self.point_now = None
        self.point_lock = None

        self.pen = QPen(col_one)
        self.delay.setChecked(False)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if point_zat or circle:
            get_pixel(event.scenePos())
        else:
            add_point(event.scenePos())


def set_flag_zat(win):
    global point_zat
    point_zat = True
    win.lock.setDisabled(True)
    win.erase.setDisabled(True)
    win.paint.setDisabled(True)
    win.addpoint.setDisabled(True)
    win.addpoint.setDisabled(True)
    win.addcircle.setDisabled(True)


def set_flag_cir(win):
    global circle
    circle = True
    win.lock.setDisabled(True)
    win.erase.setDisabled(True)
    win.paint.setDisabled(True)
    win.addpoint.setDisabled(True)
    win.addpoint.setDisabled(True)
    win.pixel.setDisabled(True)


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(point):
    global w
    if w.point_now is None:
        w.point_now = point
        w.point_lock = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
    else:
        w.edges.append([w.point_now.x(), w.point_now.y(),
                        point.x(), point.y()])
        w.point_now = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
        item_x = w.table.item(i-1, 0)
        item_y = w.table.item(i-1, 1)
        w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)
    #print(w.edges)


def lock(win):
    win.edges.append([win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y()])
    win.scene.addLine(win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now = None
    #print(win.edges)


def clean_all(win):
    win.scene.clear()
    win.table.clear()
    win.edges = []
    win.point_now = None
    win.point_lock = None
    point_zat = False
    win.image.fill(col_zero)
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)


def draw_edges(image, edges):
    p = QPainter()
    p.begin(image)
    p.setPen(QPen(QColor(0, 0, 255)))
    for ed in edges:
        p.drawLine(ed[0], ed[1], ed[2], ed[3])
    p.end()


def draw_circle(image, rad, point):
    p = QPainter()
    p.begin(image)
    p.setPen(QPen(QColor(0, 0, 255)))
    p.drawEllipse(point.x() - rad, point.y() - rad, rad * 2, rad * 2)
    p.end()


def delay():
    #QCoreApplication.processEvents(QEventLoop.AllEvents, 1)
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)
    #time.sleep(.005)

    """t = QTime.currentTime().addMSecs(1)
    while QTime.currentTime() < t:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 1)"""


def add_point_by_btn(win):
    x = win.x.value()
    y = win.y.value()
    p = QPoint()
    p.setX(x)
    p.setY(y)
    add_point(p)


def get_pixel(point):
    global w, point_zat, circle
    pix = QPixmap()
    if circle:
        r = w.rad.value()
        draw_circle(w.image, r, point)
        circle = False
    if point_zat:
        w.p_x.setValue(point.x())
        w.p_y.setValue(point.y())
        draw_edges(w.image, w.edges)
        point_zat = False
    pix.convertFromImage(w.image)
    w.scene.addPixmap(pix)
    w.lock.setDisabled(False)
    w.erase.setDisabled(False)
    w.paint.setDisabled(False)
    w.addpoint.setDisabled(False)
    w.addcircle.setDisabled(False)
    w.pixel.setDisabled(False)


def fill_with_seed(win):

    pix = QPixmap()

    paint = QPainter()
    paint.begin(win.image)

    stack = []

    edge = QColor(0, 0, 255).rgb()
    fill = QColor(0, 0, 0).rgb()
    #paint.setPen(QPen(fill))

    z = QPointF(win.p_x.value(), win.p_y.value())
    stack.append(z)

    # пока стек не пуст

    while stack:
        # извлечение пикселя (х,у) из стека
        p = stack.pop()
        x = p.x()
        y = p.y()
        # tx = x, запоминаем абсицссу
        xt = p.x()
        Fl = 0
        # цвет(х,у) = цвет закраски
        win.image.setPixel(x, y, fill)
        # заполняем интервал слева от затравки
        x = x - 1
        while win.image.pixel(x, y) != edge:
            win.image.setPixel(x, y, fill)
            x = x - 1

        # сохраняем крайний слева пиксел
        xl = x + 1
        x = xt
        # заполняем интервал справа от затравки
        x = x + 1

        while win.image.pixel(x, y) != edge:
            win.image.setPixel(x, y, fill)
            x = x + 1
        # сохраняем крайний справа пиксел
        xr = x - 1
        y = y + 1
        x = xl
        # ищем затравку на строке выше
        while x <= xr:
            Fl = 0
            while win.image.pixel(x, y) != edge and  win.image.pixel(x, y) != fill and  x <= xr:
                if Fl == 0:
                    Fl = 1
                x = x + 1

            if Fl == 1:
                if x == xr and win.image.pixel(x, y) != fill and win.image.pixel(x, y) != edge:
                    stack.append(QPointF(x, y))
                else:
                    stack.append(QPointF(x - 1, y))
                Fl = 0


            xt = x
            while (win.image.pixel(x, y) == edge or win.image.pixel(x, y) == fill) and x < xr:
                x = x + 1

            if x == xt:
                x = x + 1

        y = y - 2
        x = xl
        while x <= xr:
            Fl = 0
            while win.image.pixel(x, y) != edge and win.image.pixel(x, y) != fill and x <= xr:
                if Fl == 0:
                    Fl = 1
                x = x + 1


            if Fl == 1:
                if x == xr and win.image.pixel(x, y) != fill and win.image.pixel(x, y) != edge:
                    stack.append(QPointF(x, y))
                else:
                    stack.append(QPointF(x - 1, y))
                Fl = 0


            xt = x
            while (win.image.pixel(x, y) == edge or win.image.pixel(x, y) == fill) and x < xr:
                x = x + 1

            if x == xt:
                x = x + 1

        if win.delay.isChecked():
            delay()
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)

    if not win.delay.isChecked():
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())