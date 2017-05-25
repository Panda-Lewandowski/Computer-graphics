from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform, QPolygonF
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
import copy

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
        self.poly.clicked.connect(lambda : set_pol(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.ect.clicked.connect(lambda: add_bars(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.clip = []
        self.pol = []
        self.point_now_clip = None
        self.point_now_pol = None
        self.point_lock_pol = None
        self.point_lock_clip = None
        self.input_pol = False
        self.input_clip = False
        self.pen = QPen(black)


class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())

    def mouseMoveEvent(self, event):
        global w
        x = event.scenePos().x()
        y = event.scenePos().y()
        w.x.setText("{0}".format(x))
        w.y.setText("{0}".format(y))


def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def set_pol(win):
    if win.input_pol:
        win.input_pol = False
        win.rect.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
    else:
        win.input_pol = True
        win.rect.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def set_rect(win):
    if win.input_clip:
        win.input_clip = False
        win.poly.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
    else:
        win.input_clip = True
        win.poly.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def add_point(point):
    global w
    if w.input_clip:
        w.pen.setColor(black)
        if w.point_now_clip is None:
            w.point_now_clip = point
            w.point_lock_clip = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
        else:
            w.clip.append(point)
            w.point_now_clip = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
            item_x = w.table_rect.item(i-1, 0)
            item_y = w.table_rect.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)

    if w.input_pol:
        w.pen.setColor(blue)
        if w.point_now_pol is None:
            w.point_now_pol = point
            w.point_lock_pol = point
            add_row(w.table_pol)
            i = w.table_pol.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_pol.setItem(i, 0, item_x)
            w.table_pol.setItem(i, 1, item_y)
        else:
            w.pol.append(point)
            w.point_now_pol = point
            add_row(w.table_pol)
            i = w.table_pol.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_pol.setItem(i, 0, item_x)
            w.table_pol.setItem(i, 1, item_y)
            item_x = w.table_pol.item(i-1, 0)
            item_y = w.table_pol.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)


def lock(win):
    if w.input_pol:
        win.pol.append(win.point_lock_pol)
        win.scene.addLine(win.point_now_pol.x(), win.point_now_pol.y(), win.point_lock_pol.x(), win.point_lock_pol.y(), w.pen)
        win.point_now_pol = None

    if w.input_clip:
        win.clip.append(win.point_lock_clip)
        win.scene.addLine(win.point_now_clip.x(), win.point_now_clip.y(), win.point_lock_clip.x(), win.point_lock_clip.y(), w.pen)
        win.point_now_clip = None


def add_row(win_table):
    win_table.insertRow(win_table.rowCount())


def clean_all(win):
    win.scene.clear()
    win.table_rect.clear()
    win.table_pol.clear()
    win.clip = []
    win.pol = []
    win.point_now_clip = None
    win.point_now_pol = None
    win.point_lock_clip = None
    win.point_lock_pol = None
    r = win.table_rect.rowCount()
    for i in range(r, -1, -1):
        win.table_rect.removeRow(i)

    r = win.table_pol.rowCount()
    for i in range(r, -1, -1):
        win.table_pol.removeRow(i)


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


def is_intersection(ed1, ed2, norm):
    vis1 = is_visiable(ed1[0], ed2[0], ed2[1], norm)
    vis2 = is_visiable(ed1[1], ed2[0], ed2[1], norm)
    if (vis1 and not vis2) or (not vis1 and vis2):
        # ищем пересечение

        p1 = ed1[0]
        p2 = ed1[1]

        q1 = ed2[0]
        q2 = ed2[1]

        delta = (p2.x() - p1.x()) * (q1.y() - q2.y()) - (q1.x() - q2.x()) * (p2.y() - p1.y())
        delta_t = (q1.x() - p1.x()) * (q1.y() - q2.y()) - (q1.x() - q2.x()) * (q1.y() - p1.y())

        if abs(delta) <= 1e-6:
            return p2

        t = delta_t / delta

        I = QPointF()
        I.setX(ed1[0].x() + (ed1[1].x() - ed1[0].x()) * t)
        I.setY(ed1[0].y() + (ed1[1].y() - ed1[0].y()) * t)
        return I
    else:
        return False


def is_visiable(point, peak1, peak2, norm):
    v = vector([point, peak1], [peak2, peak1])
    if norm *  v <= 0:
        return True
    else:
        return False


def vector(v1, v2):
    x1 = v1[0].x() - v1[1].x()
    y1 = v1[0].y() - v1[1].y()

    x2 = v2[0].x() - v2[1].x()
    y2 = v2[0].y() - v2[1].y()

    return x1 * y2 - x2 * y1



def clipping(win):
    if len(win.clip) <= 1:
        QMessageBox.warning(win, "Ошибка!", "Отсекатель не задан!")

    if len(win.pol) <= 1:
        QMessageBox.warning(win, "Ошибка!", "Многоугольник не задан!")

    if len(win.pol) > 1 and len(win.clip) > 1:
        norm = isConvex(win.clip)
        if not norm:
            QMessageBox.warning(win, "Ошибка!", "Отсекатель не выпуклый!Операция не может быть проведена!")
        else:
            p = sutherland_hodgman(win.clip, win.pol, norm)
            if p:
                win.pen.setWidth(2)
                win.pen.setColor(red)
                win.scene.addPolygon(p, win.pen)
                win.pen.setWidth(1)


def sutherland_hodgman(clip, pol, norm):
    # дублируем начальную вершину отсекателя в конец
    clip.append(clip[0])

    s = None
    f = None
    # цикл по вершинам отсекателя
    for i in range(len(clip) - 1):
        new = []  # новый массив вершин
        for j in range(len(pol)):    # цикл по вершинам многоугольника
            if j == 0:
                f = pol[j]
            else:
                t = is_intersection([s, pol[j]], [clip[i], clip[i + 1]], norm)
                if t:
                    new.append(t)

            s = pol[j]
            if is_visiable(s,  clip[i], clip[i + 1], norm):
                    new.append(s)

        if len(new) != 0:
            t = is_intersection([s, f], [clip[i], clip[i + 1]], norm)
            if t:
                new.append(t)

            pol = copy.deepcopy(new)

    if len(pol) == 0:
        return False
    else:
        return QPolygonF(pol)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())