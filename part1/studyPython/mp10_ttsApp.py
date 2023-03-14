from gtts import gTTS
from playsound import *

text = '안녕하세요, 성명건입니다.'

tts = gTTS(text=text, lang='ko')
tts.save('./Part1/studyPython/hi.mp3')
print('완료')
playsound('./Part1/studyPython/hi.mp3')
print('음성출력완료')