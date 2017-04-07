from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt
from time import sleep


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = myScene(0, 0, 561, 581)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_Mono)
        self.image.fill(Qt.color0)

        self.addrow.clicked.connect(lambda: add_row(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: fill_xor(self))
        self.edges = []
        self.point_now = None
        self.point_lock = None
        self.pen = QPen(Qt.color1)


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
    r = win.table.rowCount()
    for i in range(r):
        win.table.removeRow(i) # TODO


def read_table(win):
    r = win.table.rowCount()
    for i in range(r):
        item_x = win.table.item(i, 0)
    for i in range(r):
        item_y = win.table.item(i, 1)


def fill_xor(win):
    pix = QPixmap()

    for ed in win.edges:
        # если горизонтальное ребро - дальше
        if ed[1] == ed[3]:
            continue
        # иначе определяем границы сканирования
        if ed[1] > ed[3]:
            start_y = int(ed[1])
            end_y = int(ed[3])
        else:
            start_y = int(ed[3])
            end_y = int(ed[1])

        for y in range(start_y, end_y + 1, -1):  # сканирующая строка
            # определяем пересечение
            inter = abs(((ed[2] - ed[0])*(y - ed[1])) / (ed[3] - ed[1]))
            print(ed, inter)
            """for x in range(win.image.width()):
                c1 = QColor(win.image.pixel(x + 1, y))
                c2 = QColor(win.image.pixel(x, y))
                if c1 == Qt.color1:
                    c1 = 1
                else:
                    c1 = 0
                if c2 == Qt.color0:
                    c2 = 0
                else:
                    c2 = 1

                print(c1^c2)
                win.image.setPixel(x + 1, y, Qt.color1)
                #win.scene.addLine(x+1, y, x+2, y, Qt.color1)"""
    pix.convertFromImage(win.image)
    win.scene.addPixmap(pix)

def delay():
    sleep(0.5)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())