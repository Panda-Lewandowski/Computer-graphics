from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import time

col_one = Qt.black
col_zero = Qt.white


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
        self.paint.clicked.connect(lambda: fill_xor(self))
        self.addpoint.clicked.connect(lambda: add_point_by_btn(self))
        self.edges = []
        self.point_now = None
        self.point_lock = None
        self.pen = QPen(col_one)
        self.delay.setChecked(False)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())


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


def find_max_y(ed):
    x_max = None
    for i in range(len(ed)):
        if x_max is None or ed[i][0] > x_max:
            x_max = ed[i][0]

        if x_max is None or ed[i][2] > x_max:
            x_max = ed[i][2]

    return x_max


def fill_xor(win):
    pix = QPixmap()
    p = QPainter()


    xm = int(find_max_y(win.edges))
    for ed in win.edges:
        p.begin(win.image)
        # если горизонтальное ребро - дальше
        if ed[1] == ed[3]:
            continue
        # иначе определяем границы сканирования
        if ed[1] > ed[3]:
            tmp = ed[1]
            ed[1] = ed[3]
            ed[3] = tmp

            tmp = ed[0]
            ed[0] = ed[2]
            ed[2] = tmp

        y = ed[1]
        end_y = ed[3]
        dx = (ed[2] - ed[0]) / (ed[3] - ed[1])
        start_x = ed[0]

        while y < end_y:
            # определяем пересечение

            x = start_x
            while x < xm:
                col = QColor(win.image.pixel(x, y))
                if col == col_zero:
                    p.setPen(QPen(col_one))
                else:
                    p.setPen(QPen(col_zero))
                p.drawPoint(x, y)
                x += 1

            start_x += dx
            y += 1

            if win.delay.isChecked():
                delay()
                pix.convertFromImage(win.image)
                win.scene.addPixmap(pix)

        if not win.delay.isChecked():
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)
        p.end()
    draw_edges(win.image, win.edges)

def add_point_by_btn(win):
    x = win.x.value()
    y = win.y.value()
    p = QPoint()
    p.setX(x)
    p.setY(y)
    add_point(p)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())