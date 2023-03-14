import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gtts import gTTS
from playsound import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPython/ttsApp.ui',self)
        self.setWindowIcon(QIcon('./part1/studyPython/set.png'))
        self.setWindowTitle('텍스트 투 스피치 V0.1') # 이름 설정
    
        self.btnQrGen.clicked.connect(self.btnbtnQrGenClicked)
        self.txtQrData.clicked.connect(self.btnbtnQrGenClicked)
        
    def btnbtnQrGenClicked(self):
        text = self.txtqrdata.text()
        if text == '':
            QMessageBox.warning(self, '경고','텍스트를 입력하세요')
            return
        tts = gTTS(text=text, lang='ko')
        tts.save('./Part1/studyPython/hi.mp3')
        playsound('./Part1/studyPython/hi.mp3')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())