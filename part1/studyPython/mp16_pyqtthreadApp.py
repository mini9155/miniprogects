import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Backgroundworker(QThread):
    proChanged = pyqtSignal(int)
    def __init__(self,count = 0, parent = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.working = True # 스레드 동작 여부
        self.count = count

    def run(self):
        # self.parent.pgbtask.setRange(0, 100)
        # for i in range(0,101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbtask.setValue(i)
        #     self.parent.txblog.append(f'스레드 출력 > {i}')
        while self.working:
            self.proChanged.emit(self.count)
            self.count += 1

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPython/threadapp.ui',self)
        self.setWindowIcon(QIcon('./part1/studyPython/set.png'))
        self.setWindowTitle('쓰레드앱 V0.1') # 이름 설정
        self.pgbtask.setValue(0)

        self.btnstart.clicked.connect(self.btnStartClicked)
        # 쓰레드 초기화
        self.worker = Backgroundworker(parent=self)
        # 백그라운드 워커에 있는 시그널을 접근 슬롯 함
        self.worker.proChanged.connect(self.procupdated)

    @pyqtSlot(int)
    def procupdated(self, count):
        self.txblog.append(f'스레드 출력 > {count}')
        self.pgbtask.setValue(count)

    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())