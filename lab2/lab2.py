import math
import sys, os
import copy

import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QPoint
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF


def transfer():
    global epi_x, epi_y, p1, p2, p3, p4, rect
    write_log()
    dx = window.spin_trans_x.value()
    dy = window.spin_trans_y.value()
    scene.clear()
    p1 = [p1[0] + dx, p1[1] + dy]
    p2 = [p2[0] + dx, p2[1] + dy]
    p3 = [p3[0] + dx, p3[1] + dy]
    p4 = [p4[0] + dx, p4[1] + dy]
    rect[0] = QPointF(p1[0], p1[1])
    rect[1] = QPointF(p2[0], p2[1])
    rect[2] = QPointF(p3[0], p3[1])
    rect[3] = QPointF(p4[0], p4[1])
    scene.addPolygon(rect, pen=p, brush=b)
    epi_x = [x + dx for x in epi_x]
    epi_y = [y + dy for y in epi_y]
    l = len(epi_x)
    for i in range(l):
        scene.addLine(epi_x[i], epi_y[i], epi_x[i] + 0.01, epi_y[i] + 0.01, pen=p)



def scale():
    global epi_x, epi_y, p1, p2, p3, p4, rect
    write_log()
    kx = window.spin_kx.value()
    sc_x = window.spin_scl_x.value()
    sc_y = window.spin_scl_y.value()
    ky = window.spin_ky.value()

    scene.clear()
    epi_x = [x * kx + (1 - kx) * sc_x for x in epi_x]
    epi_y = [y * ky + (1 - ky) * sc_y for y in epi_y]
    p1 = [p1[0] * kx + (1 - kx) * sc_x, p1[1] * ky + (1 - ky) * sc_y]
    p2 = [p2[0] * kx + (1 - kx) * sc_x, p2[1] * ky + (1 - ky) * sc_y]
    p3 = [p3[0] * kx + (1 - kx) * sc_x, p3[1] * ky + (1 - ky) * sc_y]
    p4 = [p4[0] * kx + (1 - kx) * sc_x, p4[1] * ky + (1 - ky) * sc_y]

    rect[0] = QPointF(p1[0], p1[1])
    rect[1] = QPointF(p2[0], p2[1])
    rect[2] = QPointF(p3[0], p3[1])
    rect[3] = QPointF(p4[0], p4[1])
    scene.addPolygon(rect, pen=p, brush=b)
    l = len(epi_x)
    for i in range(l):
        scene.addLine(epi_x[i], epi_y[i], epi_x[i] + 0.01, epi_y[i] + 0.01, pen=p)


def turn():
    global epi_x, epi_y, p1, p2, p3, p4, rect
    write_log()
    teta = math.radians(window.spin_deg.value())
    t_x = window.spin_turn_x.value()
    t_y = window.spin_turn_y.value()
    scene.clear()

    rect_t = QPolygonF(4)
    p1 = [t_x + (p1[0] - t_x) * math.cos(teta) + (p1[1] - t_y) * math.sin(teta),
          t_y - (p1[0] - t_x) * math.sin(teta) + (p1[1] - t_y) * math.cos(teta)]
    p2 = [t_x + (p2[0] - t_x) * math.cos(teta) + (p2[1] - t_y) * math.sin(teta),
          t_y - (p2[0] - t_x) * math.sin(teta) + (p2[1] - t_y) * math.cos(teta)]
    p3 = [t_x + (p3[0] - t_x) * math.cos(teta) + (p3[1] - t_y) * math.sin(teta),
          t_y - (p3[0] - t_x) * math.sin(teta) + (p3[1] - t_y) * math.cos(teta)]
    p4 = [t_x + (p4[0] - t_x) * math.cos(teta) + (p4[1] - t_y) * math.sin(teta),
          t_y - (p4[0] - t_x) * math.sin(teta) + (p4[1] - t_y) * math.cos(teta)]
    rect[0] = QPointF(p1[0], p1[1])
    rect[1] = QPointF(p2[0], p2[1])
    rect[2] = QPointF(p3[0], p3[1])
    rect[3] = QPointF(p4[0], p4[1])
    scene.addPolygon(rect, pen=p, brush=b)
    l = len(epi_x)
    for i in range(l):
        x1 = t_x + (epi_x[i] - t_x) * math.cos(teta) + (epi_y[i] - t_y) * math.sin(teta)
        y1 = t_y - (epi_x[i] - t_x) * math.sin(teta) + (epi_y[i] - t_y) * math.cos(teta)
        epi_x[i] = x1
        epi_y[i] = y1
        scene.addLine(epi_x[i], epi_y[i], epi_x[i] + 0.01, epi_y[i] + 0.01, pen=p)



def set():
    global epi_x, epi_y, p1, p2, p3, p4, rect
    scene.clear()
    dx = 500
    dy = 500
    kx = 10
    ky = 10
    p1 = [-10 * kx + dx, -10 * ky + dy]
    p2 = [-10 * kx + dx + 20 * kx, -10 * ky + dy]
    p3 = [-10 * kx + dx + 20 * kx, -10 * ky + dy + 20 * ky]
    p4 = [-10 * kx + dx, -10 * ky + dy + 20 * ky]

    rect[0] = QPointF(p1[0], p1[1])
    rect[1] = QPointF(p2[0], p2[1])
    rect[2] = QPointF(p3[0], p3[1])
    rect[3] = QPointF(p4[0], p4[1])
    epi_x = []
    epi_y = []
    scene.addPolygon(rect, pen=p, brush=b)
    for t in np.arange(0, 4 * math.pi, 0.001):
        x = 5 * math.cos(t) * kx - 2 * math.cos(5 / 2 * t) * kx + dx
        y = 5 * math.sin(t) * ky - 2 * math.sin(5 / 2 * t) * ky + dy
        epi_x.append(x)
        epi_y.append(y)
        scene.addLine(x, y, x + 0.01, y + 0.01, pen=p)


def write_log():
    global b_epi_x, b_epi_y, b1, b2, b3, b4, epi_x, epi_y, p1, p2, p3, p4, btn_undo
    b_epi_x = epi_x[:]
    b_epi_y = epi_y[:]
    b1 = p1
    b2 = p2
    b3 = p3
    b4 = p4



def undo():
    global b_epi_x, b_epi_y, b1, b2, b3, b4, epi_x, epi_y, p1, p2, p3, p4, btn_undo
    epi_x = b_epi_x
    epi_y = b_epi_y
    p1 = b1
    p2 = b2
    p3 = b3
    p4 = b4
    rect[0] = QPointF(p1[0], p1[1])
    rect[1] = QPointF(p2[0], p2[1])
    rect[2] = QPointF(p3[0], p3[1])
    rect[3] = QPointF(p4[0], p4[1])
    scene.clear()
    scene.addPolygon(rect, pen=p, brush=b)
    l = len(epi_x)
    for i in range(l):
        scene.addLine(epi_x[i], epi_y[i], epi_x[i] + 0.01, epi_y[i] + 0.01, pen=p)


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('window.ui')
scene = QtWidgets.QGraphicsScene(10, 10, 1000, 1000)
window.image.setScene(scene)
epi_x = []
epi_y = []
b_epi_x = []
b_epi_y = []
b1 = None
b2 = None
b3 = None
b4 = None
rect = QPolygonF(4)
scene.clear()
p = QPen(Qt.SolidLine)
p.setColor(Qt.black)
p.setWidth(1.5)
b = QBrush(QColor('#E6E6FA'))
set()
window.btn_trans.clicked.connect(transfer)
window.btn_scale.clicked.connect(scale)
window.btn_turn.clicked.connect(turn)
window.btn_back.clicked.connect(set)
window.btn_undo.clicked.connect(undo)
window.show()


sys.exit(app.exec_())
