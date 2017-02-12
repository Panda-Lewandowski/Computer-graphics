import sys, random
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QToolTip,
                             QDesktopWidget, QHBoxLayout, QVBoxLayout, QMainWindow,
                             )
from PyQt5.QtGui import QFont, QPainter, QColor,QImage
from PyQt5.QtCore import QCoreApplication, Qt
import math
import numpy as np


class window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):





        vbox = QVBoxLayout()
        vbox.addStretch(10)
        self.setLayout(vbox)


        sclbtn = QPushButton('Рисовать', self)
        sclbtn.setToolTip('Эта кнопка изменяет масштаб изображения')
        #sclbtn.clicked.connect(self.buttonClicked)
        sclbtn.resize(sclbtn.sizeHint())  # рекомендуемый размер кнопки

        qbtn = QPushButton('Выход', self)
        qbtn.setToolTip('Эта кнопка закрывает приложение')
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        vbox.addWidget(sclbtn)
        vbox.addWidget(qbtn)

        self.setGeometry(0, 30, 500, 500)
        self.setWindowTitle('Buttons')

    def paintEvent(self, lol):  # когда меняется размер выполняется вот это, почти как луп
        qp = QPainter()
        qp.begin(self)

        qp.end()

    """def buttonClicked(self):
        sender = self.sender()
        if sender.text() == 'Рисовать':
            qp = QPainter(self)
            qp.begin(self)
            qp.setPen(Qt.red)

            for t in np.arange(0, 4*math.pi - 0.2, 0.001):
                x = 52 * math.cos(t) - 21 * math.cos(52 / 21 * t) + 150
                y = 52 * math.sin(t) - 21 * math.sin(52 / 21 * t) + 150
                print('loololo')
                qp.drawPoint(x, y)
            qp.end()"""



class Epicycloid(QImage):

    def __init__(self):
        super().__init__()
        self.color = QColor(0, 0, 0)
        self.from_t = 0
        self.to_t = 4*math.pi
        self.center = [0, 0]
        self.put()

    def put(self):
        qp = QPainter(self)
        qp.begin(self)
        qp.setPen(self.color)

        for t in np.arange(self.from_t, self.to_t-0.2, 0.001):
            x = 52 * math.cos(t) - 21 * math.cos(52 / 21 * t) + 150
            y = 52 * math.sin(t) - 21 * math.sin(52 / 21 * t) + 150
            print('loololo')
            qp.drawPoint(x, y)
        qp.end()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = window()
    sys.exit(app.exec_())
