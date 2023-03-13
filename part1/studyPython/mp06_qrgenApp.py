# QR코드 생성
import qrcode

qr_data = 'https://python.org'
qr_image = qrcode.make(qr_data)

qr_image.save('./Part1/studyPython/site.png')

# qrcode.run_example(data='https://www.naver.com')