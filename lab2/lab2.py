import math
import sys

import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF


def set():
    global epi_x, epi_y, rect_x, rect_y, rect_w, rect_h, scene
    dx = 225
    dy = 215
    kx = 10
    ky = 10
    epi_x = []
    epi_y = []
    scene.clear()
    p = QPen(Qt.SolidLine)
    p.setColor(Qt.black)
    p.setWidth(1.5)
    b = QBrush(QColor('#E6E6FA'))
    rect = QPolygonF(4)
    rect_x = -10 * kx + dx
    rect_y = -10 * ky + dy
    rect_w = 20 * kx
    rect_h = 20 * ky
    rect[0] = QPoint(rect_x, rect_y)
    rect[1] = QPoint(rect_x + rect_w, rect_y)
    rect[2] = QPoint(rect_x + rect_w, rect_y + rect_h)
    rect[3] = QPoint(rect_x, rect_y + rect_h)
    scene.addPolygon(rect, pen=p, brush=b)
    for t in np.arange(0, 4 * math.pi, 0.001):
        x = 5 * math.cos(t) * kx - 2 * math.cos(5 / 2 * t) * kx + dx
        y = 5 * math.sin(t) * ky - 2 * math.sin(5 / 2 * t) * ky + dy
        epi_x.append(x)
        epi_y.append(y)
        scene.addLine(x, y, x + 0.01, y + 0.01, pen=p)


def draw(sc_x, sc_y, tr_x, tr_y):
    global epi_x, epi_y, rect_x, rect_y, rect_w, rect_h
    scene.clear()
    p = QPen(Qt.SolidLine)
    p.setColor(Qt.black)
    p.setWidth(1.5)
    b = QBrush(QColor('#E6E6FA'))
    rect_x = rect_x * sc_x + tr_x
    rect_y = rect_y * sc_y + tr_y
    rect_w = rect_w * sc_x
    rect_h = rect_h * sc_y
    rect = QPolygonF(4)
    rect[0] = QPoint(rect_x, rect_y)
    rect[1] = QPoint(rect_x + rect_w, rect_y)
    rect[2] = QPoint(rect_x + rect_w, rect_y + rect_h)
    rect[3] = QPoint(rect_x, rect_y + rect_h)
    scene.addPolygon(rect, pen=p, brush=b)
    epi_x = [x * sc_x + tr_x for x in epi_x]
    epi_y = [y * sc_x + tr_y for y in epi_y]
    l = len(epi_x)
    for i in range(l):
        scene.addLine(epi_x[i], epi_y[i], epi_x[i] + 0.01, epi_y[i] + 0.01, pen=p)


def transfer():
    global epi_x, epi_y, rect
    dx = window.spin_trans_x.value()
    dy = window.spin_trans_y.value()
    #print(rect_x)
    draw(1, 1, dx, dy)
    pass


def change_scale():
    global epi_x, epi_y, rect_h, rect_w, rect_x, rect_y
    kx = window.slider_kx.value()/10
    sc_x = window.spin_scl_x.value()
    sc_y = window.spin_scl_y.value()
    ky = window.slider_ky.value()/10
    scene.clear()
    p = QPen(Qt.SolidLine)
    p.setColor(Qt.black)
    p.setWidth(1.5)
    b = QBrush(QColor('#E6E6FA'))
    pre_x = [x * kx + (1-kx) * sc_x for x in epi_x]
    pre_y = [y * ky + (1-ky) * sc_y for y in epi_y]
    rect_x_t = rect_x * kx + (1-kx) * sc_x
    rect_y_t = rect_y * ky + (1-ky) * sc_y
    rect_w_t = rect_w * kx
    rect_h_t = rect_h * ky
    rect = QPolygonF(4)
    rect[0] = QPoint(rect_x_t, rect_y_t)
    rect[1] = QPoint(rect_x_t + rect_w_t, rect_y_t)
    rect[2] = QPoint(rect_x_t + rect_w_t, rect_y_t + rect_h_t)
    rect[3] = QPoint(rect_x_t, rect_y_t + rect_h_t)
    scene.addPolygon(rect, pen=p, brush=b)
    l = len(pre_x)
    for i in range(l):
        scene.addLine(pre_x[i], pre_y[i], pre_x[i] + 0.01, pre_y[i] + 0.01, pen=p)


def mem_scale():
    global epi_x, epi_y, rect_h, rect_w, rect_x, rect_y
    #print('mememory')
    kx = window.slider_kx.value() / 10
    sc_x = window.spin_scl_x.value()
    sc_y = window.spin_scl_y.value()
    ky = window.slider_ky.value() / 10
    epi_x = [x * kx + (1 - kx) * sc_x for x in epi_x]
    epi_y = [y * ky + (1 - ky) * sc_y for y in epi_y]
    #print(rect_x)
    rect_x = rect_x * kx + (1 - kx) * sc_x
    rect_y = rect_y * ky + (1 - ky) * sc_y
    rect_h *= ky
    rect_w *= kx


def change_turn():
    global epi_x, epi_y, rect_h, rect_w, rect_x, rect_y
    teta = math.radians(window.dial.value())
    t_x = window.spin_turn_x.value()
    t_y = window.spin_turn_y.value()
    scene.clear()
    p = QPen(Qt.SolidLine)
    p.setColor(Qt.black)
    p.setWidth(1.5)
    b = QBrush(QColor('#E6E6FA'))
    rect_t = QPolygonF(4)
    rect_t[0] = QPoint(t_x + (rect_x - t_x) * math.cos(teta) + (rect_y - t_y) * math.sin(teta),
                  t_y - (rect_x - t_x) * math.sin(teta) + (rect_y - t_y) * math.cos(teta))
    rect_t[1] = QPoint(t_x + (rect_x + rect_w - t_x) * math.cos(teta) + (rect_y - t_y) * math.sin(teta),
                  t_y - (rect_x + rect_w - t_x) * math.sin(teta) + (rect_y - t_y) * math.cos(teta))
    rect_t[2] = QPoint(t_x + (rect_x + rect_w - t_x) * math.cos(teta) + (rect_y + rect_h - t_y) * math.sin(teta),
                  t_y - (rect_x + rect_w - t_x) * math.sin(teta) + (rect_y + rect_h - t_y) * math.cos(teta))
    rect_t[3] = QPoint(t_x + (rect_x  - t_x) * math.cos(teta) + (rect_y + rect_h - t_y) * math.sin(teta),
                     t_y - (rect_x  - t_x) * math.sin(teta) + (rect_y + rect_h - t_y) * math.cos(teta))
    scene.addPolygon(rect_t, pen=p, brush=b)
    l = len(epi_x)
    for i in range(l):
        x1 = t_x + (epi_x[i] - t_x) * math.cos(teta) + (epi_y[i] - t_y) * math.sin(teta)
        y1 = t_y - (epi_x[i] - t_x) * math.sin(teta) + (epi_y[i] - t_y) * math.cos(teta)
        scene.addLine(x1, y1, x1 + 0.01, y1 + 0.01, pen=p)


def mem_turn():
    # TODO
    pass


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('window.ui')
scene = QtWidgets.QGraphicsScene(0, 0, 451, 431)
window.image.setScene(scene)
epi_x = None
epi_y = None

set()
window.btn_trans.clicked.connect(transfer)
window.btn_scale.clicked.connect(mem_scale)
window.btn_turn.clicked.connect(mem_turn)
window.btn_back.clicked.connect(set)
window.slider_kx.valueChanged.connect(change_scale)
window.slider_ky.valueChanged.connect(change_scale)
window.dial.valueChanged.connect(change_turn)
window.show()
sys.exit(app.exec_())
