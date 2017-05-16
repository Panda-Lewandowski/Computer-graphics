from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
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


def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


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
    win.edges.append(win.point_lock)
    win.scene.addLine(win.point_now_rect.x(), win.point_now_rect.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now_rect = None


def clean_all(win):
    win.scene.clear()
    win.table_rect.clear()
    win.table_bars.clear()
    win.lines = []
    win.edges = []
    win.point_now_rect = None
    win.point_now_bars = None
    win.point_lock = None
    win.image.fill(Qt.white)
    r = win.table_rect.rowCount()
    for i in range(r, -1, -1):
        win.table_rect.removeRow(i)

    r = win.table_bars.rowCount()
    for i in range(r, -1, -1):
        win.table_bars.removeRow(i)


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
            w.edges.append(point)
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


def clipping(win):
    norm = isConvex(win.edges)
    if not norm:
        QMessageBox.warning(win, "Ошибка!", "Отсекатель не выпуклый!Операция не может быть проведена!")

    for b in win.lines:
        win.pen.setColor(blue)
        cyrus_beck(b, win.edges, norm, win.scene, win.pen)
    win.pen.setColor(red)


def isConvex(edges):
    flag = 1

    # начальные вершины
    vo = edges[0]  # iая вершина
    vi = edges[1]  # i+1 вершина
    vn = edges[2]  # i+2 вершина и все остальные

    # векторное произведение двух векторов
    x1 = vi.x() - vo.x()
    y1 = vi.y() - vo.y()

    x2 = vn.x() - vi.x()
    y2 = vn.y() - vi.y()

    # определяем знак ординаты
    r = x1 * y2 - x2 * y1
    prev = sign(r)

    for i in range(2, len(edges) - 1):
        if not flag:
            break
        vo = edges[i - 1]
        vi = edges[i]
        vn = edges[i + 1]

        # векторное произведение двух векторов
        x1 = vi.x() - vo.x()
        y1 = vi.y() - vo.y()

        x2 = vn.x() - vi.x()
        y2 = vn.y() - vi.y()

        r = x1 * y2 - x2 * y1
        curr = sign(r)

        # если знак предыдущей координаты не совпадает, то возможно многоугольник невыпуклый
        if curr != prev:
            flag = 0
        prev = curr

    # не забываем проверить последнюю с первой вершины
    vo = edges[len(edges) - 1]
    vi = edges[0]
    vn = edges[1]

    # векторное произведение двух векторов
    x1 = vi.x() - vo.x()
    y1 = vi.y() - vo.y()

    x2 = vn.x() - vi.x()
    y2 = vn.y() - vi.y()

    r = x1 * y2 - x2 * y1
    curr = sign(r)
    if curr != prev:
        flag = 0

    return flag * curr


def scalar(v1, v2):
    return v1.x() * v2.x() + v1.y() * v2.y()


def cyrus_beck(r, edges, n, scene, p):
    # инициализируем пределы значений параметра, предполагая, что весь отрезок полностью видимый
    # максимизируем t нижнее и t верхнее, исходя из того что 0 <= t <= 1
    tb = 0
    te = 1

    # вычисляем директрису(определяет направление/ориентацию отрезка) D= p1 - p2
    D = QPointF()
    D.setX(r[1][0] - r[0][0])
    D.setY(r[1][1] - r[0][1])

    # главный цикл по сторонам отсекателя
    for i in range(len(edges)):
        # вычисляем wi, D * ni, wi * n
        # весовой множитель удаленности гранничной точки от р1(берем граничную точку равной вершине)
        W = QPointF()
        W.setX(r[0][0] - edges[i].x())
        W.setY(r[0][1] - edges[i].y())

        # определяем нормаль
        N = QPointF()
        if i == len(edges) - 1:
            N.setX(-n * (edges[0].y() - edges[i].y()))
            N.setY(n * (edges[0].x() - edges[i].x()))
        else:
            N.setX(-n * (edges[i + 1].y() - edges[i].y()))
            N.setY(n * (edges[i + 1].x() - edges[i].x()))
        # определяем скалярные произведения
        Dscalar = scalar(D, N)
        Wscalar = scalar(W, N)

        if Dscalar == 0:
            # если отрезок выродился в точку
            if Wscalar < 0:
                # видна ли точка относительно текущей границы?
                break
        else:
            # отрезок невырожден, определяем t
            t = - Wscalar / Dscalar
            # поиск верхнего и нижнего предела t

            if Dscalar > 0:
                # поиск нижнего предела
                # верно ли, что t <= 1
                if t > 1:
                    return
                else:
                    tb = max(tb, t)
            elif Dscalar < 0:
                # поиск верхнего предела
                # верно ли, что t >= 0
                if t < 0:
                    return
                else:
                    te = min(te, t)

        # проверка фактической видимости отрезка
    if tb <= te:
        scene.addLine(r[0][0] + (r[1][0] - r[0][0]) * te,
                      r[0][1] + (r[1][1] - r[0][1]) * te,
                      r[0][0] + (r[1][0] - r[0][0]) * tb,
                      r[0][1] + (r[1][1] - r[0][1]) * tb, p)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
