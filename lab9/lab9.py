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
        self.pol.clicked.connect(lambda : set_pol(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.ect.clicked.connect(lambda: add_bars(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.pol_clip = []
        self.pol_pol = []
        self.clip = None
        self.point_now_rect = None
        self.point_now_pol = None
        self.point_lock_pol = None
        self.point_lock_rect = None
        self.input_pol = False
        self.input_rect = False
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
    if win.input_rect:
        win.input_rect = False
        win.pol.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
    else:
        win.input_rect = True
        win.pol.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def add_point(point):
    global w
    if w.input_rect:
        w.pen.setColor(black)
        if w.point_now_rect is None:
            w.point_now_rect = point
            w.point_lock_rect = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
        else:
            w.pol_clip.append(point)
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
            w.pol_pol.append(point)
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
        win.pol_clip.append(win.point_lock_pol)
        win.scene.addLine(win.point_now_pol.x(), win.point_now_pol.y(), win.point_lock_pol.x(), win.point_lock_pol.y(), w.pen)
        win.point_now_pol = None

    if w.input_rect:
        win.pol_pol.append(win.point_lock_rect)
        win.scene.addLine(win.point_now_rect.x(), win.point_now_rect.y(), win.point_lock_rect.x(), win.point_lock_rect.y(), w.pen)
        win.point_now_rect = None


def add_row(win_table):
    win_table.insertRow(win_table.rowCount())


def clean_all(win):
    win.scene.clear()
    win.table_rect.clear()
    win.table_pol.clear()
    win.pol_clip = []
    win.pol_pol = []
    win.point_now_rect = None
    win.point_now_pol = None
    win.point_lock_rect = None
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


def clipping(win):
    if len(win.pol_clip) <= 1:
        QMessageBox.warning(win, "Ошибка!", "Отсекатель не задан!")

    if len(win.pol_pol) <= 1:
        QMessageBox.warning(win, "Ошибка!", "Многоугольник не задан!")

    if len(win.pol_pol) > 1 and len(win.pol_clip) > 1:
        norm = isConvex(win.pol_clip)
        if not norm:
            QMessageBox.warning(win, "Ошибка!", "Отсекатель не выпуклый!Операция не может быть проведена!")
        else:
            p = sutherland_hodgman(win.pol_clip, win.pol_pol, norm)
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
    for i in range(len(clip) - 1):
        new = []
        for j in range(len(pol)):
            if j == 0:
                f = pol[j]
            else:
                t = is_intersection([s, pol[j]], [clip[i], clip[i + 1]])
                if t:
                    new.append(t)

            s = pol[j]
            if is_visiable(s,  clip[i], clip[i + 1]):
                    new.append(s)

        if len(new) != 0:
            t = is_intersection([s, f], [clip[i], clip[i + 1]])
            if t:
                new.append(t)
            print(new)
            new.append(new[0])
            pol = copy.deepcopy(new)

    if len(pol) == 0:
        return False
    else:
        return QPolygonF(pol)


def is_intersection(ed1, ed2):
    if (is_visiable(ed1[0], ed2[0], ed2[1]) and not is_visiable(ed1[1], ed2[0], ed2[1])) or \
            (not is_visiable(ed1[0], ed2[0], ed2[1]) and is_visiable(ed1[1], ed2[0], ed2[1])):
        # ищем пересечение
        a = ed1[0].x()
        b = ed1[1].x() - ed1[0].x()
        c = ed2[0].x()
        d = ed2[1].x() - ed2[0].x()

        e = ed1[0].y()
        f = ed1[1].y() - ed1[0].y()
        p = ed2[0].y()
        m = ed2[1].y() - ed2[0].y()

        t = (d * (e + p) - m * (a + c))/(d * f - b * m)
        #print(t)

        if 0 <= t <= 1:
            I = QPointF()
            I.setX(ed1[0].x() + (ed1[1].x() - ed1[0].x()) * t)
            I.setY(ed1[0].y() + (ed1[1].y() - ed1[0].y()) * t)
            #print(I.x(), I.y())
            return I
        else:
            return False

    else:
        return False


def is_visiable(point, peak1, peak2):
    """if line(peak1, peak2, point) * line(peak1, peak2, peak3) < 0:
            return False
        else:
            return True"""

    """W = QPointF()
    W.setX(point.x() - peak1.x())
    W.setY(point.y() - peak1.y())

    N = QPointF()
    N.setX(-n * (peak2.y() - peak1.y()))
    N.setY(n * (peak2.x() - peak1.x()))

    Wscalar = scalar(W, N)
    if Wscalar >= 0:
        return True
    else:
        return False"""
    if vector([peak1, point], [peak1, peak2]) >= 0:
        return True
    else:
        return False


def vector(v1, v2):
    x1 = v1[0].x() - v1[1].x()
    y1 = v1[0].y() - v1[1].y()

    x2 = v2[0].x() - v2[1].x()
    y2 = v2[0].y() - v1[1].y()

    r = x1 * y2 - x2 * y1
    return sign(r)




def scalar(v1, v2):
    return v1.x() * v2.x() + v1.y() * v2.y()


def line(p1, p2, p):
    if (p1.y() - p2.y()) * p.x() + (p2.x() - p1.x()) * p.y() + (p1.x() * p2.y() - p2.x() * p1.y()) >= 0:
        return 1
    else:
        return -1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())