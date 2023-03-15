import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

MAX = 10000
class Backgroundworker(QThread):
    proChanged = pyqtSignal(int) # 커스텀 시그널
    def __init__(self,count = 0, parent = None) -> None:
        super().__init__()
        self.main = parent
        self.working = False # 스레드 동작 여부
        self.count = count

    def run(self):
        # self.parent.pgbtask.setRange(0, 100)
        # for i in range(0,101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbtask.setValue(i)
        #     self.parent.txblog.append(f'스레드 출력 > {i}')
        while self.working:
            if self.count <= MAX:
                self.proChanged.emit(self.count) # 시그널 내보냄
                self.count += 1 # 값 증가만 // 업무프로세스 동작하는 위치
                time.sleep(0.001) # 세밀하게 주면 GUI 처리를 못함
            else:
                self.working = False
class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPython/threadapp.ui',self)
        self.setWindowIcon(QIcon('./part1/studyPython/set.png'))
        self.setWindowTitle('쓰레드앱 V0.1') # 이름 설정
        self.pgbtask.setValue(0)

        self.btnstart.clicked.connect(self.btnStartClicked)
        # 쓰레드 생성
        self.worker = Backgroundworker(parent=self)
        # 백그라운드 워커에 있는 시그널을 접근 슬롯 함
        self.worker.proChanged.connect(self.procupdated)
        self.pgbtask.setRange(0,MAX)

#    @pyqtSlot(int)
    def procupdated(self, count):
        self.txblog.append(f'스레드 출력 > {count}')
        self.pgbtask.setValue(count)
        print(f'스레드 출력 > {count}')
#    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start() # 스레드 클래스
        self.worker.working = True
        self.worker.count = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())