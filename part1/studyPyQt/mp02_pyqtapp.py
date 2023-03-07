# Qt Designer 디자인 사용
import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class qtApp(QWidget):
    count = 0 # 클릭횟수 카운트 변수

    def __init__(self):
        super().__init__()
        uic.loadUi('C:\source\miniprogects\part1\studyPyQt\mainApp.ui',self)
        
        # Qt Designer에서 구상한 위젯 시그널을 만듬
        self.btnOK.clicked.connect(self.btnOkclicked)
        self.btnPOP.clicked.connect(self.btnPOPClicked)

    def btnPOPClicked(self):
        QMessageBox.about(self,'popup','까꿍!') # (self, 창 제목, 창 내용)

    def btnOkclicked(self):
        self.count += 1
        self.lblMessage.clear()
        self.lblMessage.setText(f'메세지:OK!!!+{self.count}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())