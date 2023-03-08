# Qt Designer 디자인 사용
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser # 웹브라우저 모듈
from urllib.request import urlopen


class qtApp(QWidget):

    def __init__(self):
        super().__init__()
        uic.loadUi('C:/source/miniprogects/part1/studyPyQt/naverApimovie.ui',self)
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
        url = self.tblresult.item(selected, 5).text()
        webbrowser.open(url) # 뉴스기사 웹사이트 오픈
        # print(url)

    def txtSearchReturned(self):
        self.btnSearchClicked()

    def btnSearchClicked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self,'경고','영화명을 입력하세요!')
            return
        else:
            api = NaverApi() # NaverApi 클래스
            node = 'movie' # movie로 변경하면 영화 검색
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            print(result)
            # print(result)
            # x테이블위젯에 출력 가능
            items = result['items'] # json 결과 중에서 items 아래 배열만 추출
            self.makeTable(items) # 테이블위젯에 데이터들을 할당

    #테이블 위젯에 데이터 표시
    def makeTable(self, items) -> None:
        self.tblresult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblresult.setColumnCount(7)
        self.tblresult.setRowCount(len(items)) # 현재 100개 행 생성
        self.tblresult.setHorizontalHeaderLabels(['영화제목','개봉연도','감독','배우진','평점','링크','포스터'])
        self.tblresult.setColumnWidth(0,150)
        self.tblresult.setColumnWidth(1,60)
        self.tblresult.setColumnWidth(4,50)

        # 컬럼데이터를 수정 금지
        self.tblresult.setEditTriggers(QAbstractItemView.NoEditTriggers)


        for i,post in enumerate(items): #0, 영화
            title = self.replaceHtmlTag(post['title'])
            pubDate = post['pubDate']
            director = post['director']
            link = post['link']
            actor = post['actor']
            userRating = post['userRating']
            # image = QImage(requests.get(post['image'],stream = True))
            imageurl = urlopen(post['image']).read()
            image = QPixmap()
            image.loadFromData(imageurl)
            imglabel = QLabel()
            imglabel.setPixmap(QPixmap.fromImage(image))
            imglabel.setGeometry(0,0,60,100)
            imglabel.resize(60,100)
            # setItem(행,열, 넣을 데이터
            self.tblresult.setItem(i, 0 ,QTableWidgetItem(title))
            self.tblresult.setItem(i, 1 ,QTableWidgetItem(pubDate))
            self.tblresult.setItem(i, 2 ,QTableWidgetItem(director))
            self.tblresult.setItem(i, 3 ,QTableWidgetItem(actor))
            self.tblresult.setItem(i, 4 ,QTableWidgetItem(userRating))
            self.tblresult.setItem(i, 5 ,QTableWidgetItem(link))
            self.tblresult.setCellWidget(i, 6 ,imglabel)


    def replaceHtmlTag(self, sentence) -> str:
        result = sentence.replace('&lt;','<').replace('&gt;','>').replace('<b>','') .replace('</b>','').replace('&apos;',"'").replace('&quot;','"')
        # 변환 안 된 특수문자가 나타나면 여기에 추가

        return result




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())