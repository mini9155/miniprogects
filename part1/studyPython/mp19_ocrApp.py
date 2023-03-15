# 글자추출
# 이미지 처리 모듈 pip install pillow
# OCR 모듈 pip install pytesseract
from PIL import Image
import pytesseract as tess

img_path = './part1/studyPython/study.png'
tess.pytesseract.tesseract_cmd = 'C:/DEV/tools/Tesseract-OCR/tesseract.exe'

result = tess.image_to_string(Image.open(img_path), lang='kor')
print(result)