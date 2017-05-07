from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import time

red = Qt.red
blue = Qt.blue
black = Qt.black
now = None

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 561, 581)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.bars.clicked.connect(lambda : set_bars(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.ect.clicked.connect(lambda: add_bars(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.lines = []
        self.edges = []
        self.clip = None
        self.point_now_rect = None
        self.point_now_bars = None
        self.point_lock = None
        self.input_bars = False
        self.input_rect = False
        self.pen = QPen(black)


class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())


def set_bars(win):
    if win.input_bars:
        win.input_bars = False
        win.rect.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
        win.lock.setDisabled(False)
    else:
        win.input_bars = True
        win.rect.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)
        win.lock.setDisabled(True)


def set_rect(win):
    if win.input_rect:
        win.input_rect = False
        win.bars.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
        win.lock.setDisabled(False)
    else:
        win.input_rect = True
        win.bars.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def lock(win):
    win.edges.append([win.point_now_rect.x(), win.point_now_rect.y(), win.point_lock.x(), win.point_lock.y()])
    win.scene.addLine(win.point_now_rect.x(), win.point_now_rect.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now_rect = None


def add_row(win_table):
    win_table.insertRow(win_table.rowCount())


def add_point(point):
    global w
    if w.input_rect:
        w.pen.setColor(black)
        if w.point_now_rect is None:
            w.point_now_rect = point
            w.point_lock = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
        else:
            w.edges.append([w.point_now_rect.x(), w.point_now_rect.y(),
                            point.x(), point.y()])
            w.point_now_rect = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
            item_x = w.table_rect.item(i-1, 0)
            item_y = w.table_rect.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)
    if w.input_bars:
        w.pen.setColor(red)
        if w.point_now_bars is None:
            w.point_now_bars = point
        else:
            w.lines.append([[w.point_now_bars.x(), w.point_now_bars.y()],
                            [point.x(), point.y()]])

            add_row(w.table_bars)
            i = w.table_bars.rowCount() - 1
            item_b = QTableWidgetItem("[{0}, {1}]".format(w.point_now_bars.x(), w.point_now_bars.y()))
            item_e = QTableWidgetItem("[{0}, {1}]".format(point.x(), point.y()))
            w.table_bars.setItem(i, 0, item_b)
            w.table_bars.setItem(i, 1, item_e)
            w.scene.addLine(w.point_now_bars.x(), w.point_now_bars.y(), point.x(), point.y(), w.pen)
            w.point_now_bars = None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
