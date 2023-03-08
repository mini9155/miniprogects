# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser # 웹브라우저 모듈


class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('C:/source/miniprogects/part1/studyPyQt/naverApisearch.ui',self)
        self.setWindowIcon(QIcon('C:/source/miniprogects/part1/studyPyQt/newpaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        # 검색어 입력 후 엔터를 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblresult.doubleClicked.connect(self.tblresultDoubleClicked)

    def tblresultDoubleClicked(self):
        # row = self.tblresult.currentIndex().row()
        # column  = self.tblresult.currentIndex().column()
        # # print(row, column)
        selected = self.tblresult.currentRow()
        url = self.tblresult.item(selected, 1).text()
        webbrowser.open(url) # 뉴스기사 웹사이트 오픈
        # print(url)

    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'경고','검색어를 입력하세요!')
            return
        else:
            api = NaverApi() # NaverApi 클래스
            node = 'news' # movie로 변경하면 영화 검색
            outputs = [] # 결과를 담을 변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # x테이블위젯에 출력 가능
            items = result['items'] # json 결과 중에서 items 아래 배열만 추출
            self.makeTable(items) # 테이블위젯에 데이터들을 할당

    #테이블 위젯에 데이터 표시
    def makeTable(self, items) -> None:
        self.tblresult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblresult.setColumnCount(2)
        self.tblresult.setRowCount(len(items)) # 현재 100개 행 생성
        self.tblresult.setHorizontalHeaderLabels(['기사제목','뉴스링크'])
        self.tblresult.setColumnWidth(0,310)
        self.tblresult.setColumnWidth(1,260)
        # 컬럼데이터를 수정 금지
        self.tblresult.setEditTriggers(QAbstractItemView.NoEditTriggers)


        for i,post in enumerate(items): #0, 뉴스
            title = self.replaceHtmlTag(post['title'])
            originallink = post['originallink']
            # setItem(행,열, 넣을 데이터
            self.tblresult.setItem(i, 0 ,QTableWidgetItem(title))
            self.tblresult.setItem(i, 1 ,QTableWidgetItem(originallink))

    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;','<').replace('&gt;','>').replace('<b>','') .replace('</b>','').replace('&apos;',"'").replace('&quot;','"')
        # 변환 안 된 특수문자가 나타나면 여기에 추가

        return result




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())