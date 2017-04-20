from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import time

col_one = QColor(0, 0, 0)
col_zero = QColor(255, 255, 255)
point_zat = False

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
        self.pixel.clicked.connect(set_flag)
        self.edges = []
        self.point_now = None
        self.point_lock = None

        self.pen = QPen(col_one)
        self.delay.setChecked(False)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if point_zat:
            get_pixel(event.scenePos())
        else:
            add_point(event.scenePos())


def set_flag():
    global point_zat
    point_zat = True



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
    p.setPen(QPen(col_one))
    for ed in edges:
        p.drawLine(ed[0], ed[1], ed[2], ed[3])
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
    global w
    w.p_x.setValue(point.x())
    w.p_y.setValue(point.y())


def fill_with_seed(win):
    pix = QPixmap()
    draw_edges(win.image, win.edges)
    p = QPainter()
    p.begin(win.image)
    p.setPen(QPen(col_one))
    stack = []

    z = QPoint(win.p_x.value(), win.p_y.value())
    stack.append(z)
    # пока стек не пуст
    while stack:
        print(stack)
        # извлечение пикселя (х,у) из стека
        seed = stack.pop()
        # цвет(х,у) = цвет закраски
        p.drawPoint(seed)
        # tx = x, запоминаем абсицссу
        tx = seed.x()
        x = seed.x()
        y = seed.y()

        # заполняем интервал слева от затравки
        x -= 1
        # цвет(х,у) != цвету границы
        col = win.image.pixelColor(x, y)
        while col.getRgb() != (0, 0, 0, 255) and abs(x) < 561:
            p.drawPoint(x, y)
            x -= 1
            col = win.image.pixelColor(x, y)

        # сохраняем крайний слева пиксел
        xLeft = x + 1

        x = tx
        # заполняем интервал справа от затравки
        x += 1
        # цвет(х,у) != цвету границы
        col = win.image.pixelColor(x, y)
        while col.getRgb() != (0, 0, 0, 255) and abs(x) < 581:
            p.drawPoint(x, y)
            x += 1
            col = win.image.pixelColor(x, y)

        # сохраняем крайний справа пиксел
        xRight = x - 1

        x = xLeft
        # ищем затравку на строке выше
        y = y + 1
        fill_line(win, stack, xRight, x, y)
        # ищем затравку на строке ниже
        y = y - 1
        fill_line(win, stack, xRight, x, y)

        if win.delay.isChecked():
            delay()
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)

    if not win.delay.isChecked():
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)

    p.end()


def fill_line(win, stack, xRight, x, y):
    # создаем новую точку
    new = QPoint()
    while x <= xRight:
        flag = 0

        col = win.image.pixelColor(x, y)
        while col.getRgb() != (0, 0, 0, 255) and x < xRight:
            if flag == 0:
                flag = 1
            x += 1
            col = win.image.pixelColor(x, y)

        if flag:
            col = win.image.pixelColor(x, y)
            if x == xRight and col.getRgb() != (0, 0, 0, 255):
                print(1)
                new.setX(x)
                new.setY(y)
                stack.append(new)
            else:
                print(2)
                new.setX(x - 1)
                new.setY(y)
                stack.append(new)
            flag = 0
        # продолжим проверку, если интервал был прерван
        tmp = x
        col = win.image.pixelColor(x, y)
        while col.getRgb() == (0, 0, 0, 255) and x < xRight:
            x += 1

        if x == tmp:
            x += 1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())