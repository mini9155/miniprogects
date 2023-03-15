# 이메일 보내기 앱
import smtplib # 메일전송프로토콜
from email.mime.text import MIMEText

send_email = 'hanbv@naver.com'
send_pass = '-----'

recv_email = 'keyhanbv123@gmail.com'

smtp_name = 'smtp.naver.com'
smtp_port = 587 # 

text = '''메일내용입니다.긴급입니다. 조심하세요~ 빨리 연락주세요!!'''

msg = MIMEText(text)
msg['subject'] = '메일 제목입니다'
msg['From'] = send_email
msg['To'] = recv_email
print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port)
mail.starttls()
mail.login(send_email,send_pass)
mail.sendmail(send_email,recv_email, msg=msg.as_string())
mail.quit()
print('전송완료')