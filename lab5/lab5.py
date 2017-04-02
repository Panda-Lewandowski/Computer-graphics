from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = myScene(0, 0, 511, 511)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.addrow.clicked.connect(lambda: add_row(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.xss = []
        self.yss = []
        self.pen = QPen(Qt.black)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(point):
    global w
    add_row(w)
    i = w.table.rowCount() - 1
    w.xss.append(point.x())
    w.yss.append(point.y())
    item_x = QTableWidgetItem("{0}".format(point.x()))
    item_y = QTableWidgetItem("{0}".format(point.y()))
    w.table.setItem(i, 0, item_x)
    w.table.setItem(i, 1, item_y)
    item_x = w.table.item(i-1, 0)
    item_y = w.table.item(i-1, 1)
    if i:
        w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)


def lock(win):
    i = w.table.rowCount() - 1
    item_x = w.table.item(i, 0)
    item_y = w.table.item(i, 1)
    win.scene.addLine(win.xss[0], win.yss[0], float(item_x.text()), float(item_y.text()), w.pen)


def clean_all(win):
    win.scene.clear()
    win.xss = []
    win.yss = []
    win.table.clear()
    r = win.table.rowCount()
    for i in range(r):
        win.table.removeRow(i) #TODO

def read_table(win):
    win.xss = []
    win.yss = []
    r = win.table.rowCount()
    for i in range(r):
        item_x = win.table.item(i, 0)
        win.xss.append(float(item_x.text()))
    for i in range(r):
        item_y = win.table.item(i, 1)
        win.yss.append(float(item_y.text()))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())