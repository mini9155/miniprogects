# 주소록 GUI 프로그램 - MySQL 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymysql


class qtApp(QMainWindow):
    conn = None
    curIdx = 0 # 현재 데이터 PK

    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPyQt/addressBook.ui',self) # ui 불러오기
        self.setWindowIcon(QIcon('./part1/studyPyQt/addressbook.png')) # 사진 넣기
        self.setWindowTitle('주소록') # 이름 설정

        self.initDB() # DB 초기화

        self.btnNew.clicked.connect(self.btnNewClicked) # 신규 버튼 연결
        self.btnSave.clicked.connect(self.btnSaveClicked) # 저장 버튼 연결
        self.tblAddress.doubleClicked.connect(self.tblAddressDoublelicked) # 더블클릭 안되게
        self.btnDel.clicked.connect(self.btnDelClicked) # 삭제 버튼 연결



    # 삭제 버튼 누르면 전부 비우기
    def btnNewClicked(self): # 신규버튼을 누르면
        # 라인 에디트 내용 삭제 후 이름에 포커스
        self.txtName.setText('')
        self.txtPhNum.setText('')
        self.txtEmail.setText('')
        self.txtAddress.setText('')
        self.txtName.setFocus()
        self.curIdx = 0 # 0은 진짜 신규!

    def tblAddressDoublelicked(self):
        rowIndex = self.tblAddress.currentRow()
        self.txtName.setText(self.tblAddress.item(rowIndex,1).text())
        self.txtPhNum.setText(self.tblAddress.item(rowIndex,2).text())
        self.txtEmail.setText(self.tblAddress.item(rowIndex,3).text())
        self.txtAddress.setText(self.tblAddress.item(rowIndex,4).text())
        self.curIdx = int(self.tblAddress.item(rowIndex, 0).text())

    def btnSaveClicked(self): # 저장
        fullName = self.txtName.text()
        phoneNum = self.txtPhNum.text()
        email = self.txtEmail.text()
        address = self.txtAddress.text()

        # print(fullName,phoneNum,email,address)
        # 이름과 전화번호를 입력하지 않으면 알람
        if fullName == '' or phoneNum == '':
            QMessageBox.warning(self, '주의', '이름과 전화번호를 입력하세요!!!')
            return # 진행불가
        else:
            self.conn = pymysql.connect(host='localhost'
                                    , user='root'
                                    ,password='12345'
                                    , db = 'miniproject'
                                    , charset= 'utf8')
            if self.curIdx == 0:

            # 네개 변수값 받아서 INSERT 쿼리문 만들기
                query = '''INSERT INTO addressbook (FullName, PhoneNum, Email, Address)
                                VALUES (%s,%s,%s,%s)'''
            else:
                query = '''UPDATE addressbook
                                SET FullName = %s
                                , PhoneNum =%s
                                , Email = %s
                                , Address = %s
                                WHERE Idx = %s'''
            
            cur = self.conn.cursor()
            if self.curIdx == 0:
                cur.execute(query, (fullName, phoneNum, email, address))
            else:
                cur.execute(query,(fullName, phoneNum, email, address, self.curIdx)) 

            self.conn.commit()
            self.conn.close()

            if self.curIdx == 0:# 저장성공 메세지
                QMessageBox.about(self, '알림', f'{fullName}님이 주소록에 저장되었습니다')
            else:
                QMessageBox.about(self, '알림', '변경 성공 했습니다')
            # QTableWidget 새 데이터가 출력되도록
            self.initDB()
            # 입력창 내용 없어져
            self.btnNewClicked()

    def btnDelClicked(self):
        if self.curIdx == 0:
            QMessageBox.warning(self, '알림', '삭제할 데이터를 선택하시오')
            return
        else:
            reply = QMessageBox.question(self,'알림','정말로 삭제하시겠습니까?',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            
            self.conn = pymysql.connect(host='localhost'
                                        , user='root'
                                        ,password='12345'
                                        , db = 'miniproject'
                                        , charset= 'utf8')
            query = 'DELETE FROM addressbook WHERE Idx = %s'
            cur = self.conn.cursor()
            cur.execute(query, (self.curIdx))

            self.conn.commit()
            self.conn.close()
            QMessageBox.about(self, '알림', '삭제했습니다')
            
            self.initDB()
            self.btnNewClicked()

    def initDB(self):
        self.conn = pymysql.connect(host='localhost'
                                    , user='root'
                                    ,password='12345'
                                    , db = 'miniproject'
                                    , charset= 'utf8')
        cur = self.conn.cursor()
        query = '''SELECT Idx
                    , FullName
                    , PhoneNum
                    , Email
                    , Address
                    FROM addressbook;'''
 # ;을 쓰면 오류가 날 때 가 있음
        cur.execute(query)
        rows = cur.fetchall()

        self.makeTable(rows)
        self.conn.close()

    def makeTable(self,rows):
        self.tblAddress.setColumnCount(5) # 컬럼 갯수
        self.tblAddress.setRowCount(len(rows)) # 0. 행 갯수
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblAddress.setHorizontalHeaderLabels(['번호','이름','전화번호','이메일','주소'])

        for i,row in enumerate(rows):
            idx = row[0]
            fullName = row[1]
            phoneNum = row[2]
            email = row[3]
            address = row[4]


            self.tblAddress.setItem(i, 0 ,QTableWidgetItem(str(idx))) # 문자열 선언
            self.tblAddress.setItem(i, 1 ,QTableWidgetItem(fullName))
            self.tblAddress.setItem(i, 2 ,QTableWidgetItem(phoneNum))
            self.tblAddress.setItem(i, 3 ,QTableWidgetItem(email))
            self.tblAddress.setItem(i, 4 ,QTableWidgetItem(address))

            self.tblAddress.setColumnWidth(0,0)
            self.tblAddress.setColumnWidth(1,70)
            self.tblAddress.setColumnWidth(2,105)
            self.tblAddress.setColumnWidth(3,175)
            self.tblAddress.setColumnWidth(4,200)

            self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers) # 컬럼수정금지

        self.stbCurrent.showMessage(f'전체주소록:{len(rows)}개')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())