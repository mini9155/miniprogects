import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPython/threadapp.ui',self)
        self.setWindowIcon(QIcon('./part1/studyPython/set.png'))
        self.setWindowTitle('노쓰레드앱 V0.1') # 이름 설정
        self.pgbtask.setValue(0)

        self.btnstart.clicked.connect(self.btnStartClicked)

    def btnStartClicked(self):
        self.pgbtask.setRange(0,100)
        for i in range(0,101):
            print(f'노스레드 출력 > {i}')
            self.pgbtask.setValue(i)
            self.txblog.append(f'노스레드 출력 > {i}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())