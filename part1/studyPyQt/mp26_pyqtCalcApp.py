import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql
import math


class qtApp(QWidget):
    conn = None
    curIdx = 0 # 현재 데이터 PK

    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/caculator.ui',self)

        self.btn_C.clicked.connect(self.btnClicked)
        self.btn_number0.clicked.connect(self.btnClicked)
        self.btn_number1.clicked.connect(self.btnClicked)
        self.btn_number2.clicked.connect(self.btnClicked)
        self.btn_number3.clicked.connect(self.btnClicked)
        self.btn_number4.clicked.connect(self.btnClicked)
        self.btn_number5.clicked.connect(self.btnClicked)
        self.btn_number6.clicked.connect(self.btnClicked)
        self.btn_number7.clicked.connect(self.btnClicked)
        self.btn_number8.clicked.connect(self.btnClicked)
        self.btn_number9.clicked.connect(self.btnClicked)
        self.btn_result.clicked.connect(self.btnClicked)
        self.btn_minus.clicked.connect(self.btnClicked)
        self.btn_add.clicked.connect(self.btnClicked)
        self.btn_multipy.clicked.connect(self.btnClicked)
        self.btn_divide.clicked.connect(self.btnClicked)

        self.le_view.setEnabled(False)
        self.le_value = ''
        

    def btnClicked(self):
        btn_val = self.sender().text()
        if btn_val == 'C': # clear
            print('clear')
            self.le_view.setText('0')
            self.le_value = ''
        elif btn_val == '=': # 계산결과
            print('=')
            try:
                result = eval(self.le_value.lstrip('0'))
                print(round(result,4)) # 예를들어 10/6 할 때 소수점 자리 잘라주기 
                self.le_view.setText(str(round(result,4)))
            except: 
                self.le_view.setText('ERROR')
        else:
            if btn_val == 'X':
                btn_val = '*'
            self.le_value += btn_val
            print(self.le_value)
            self.le_view.setText(self.le_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())