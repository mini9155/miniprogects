import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import psutil
import socket
import requests
import re

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./part1/studyPython/cominfo.ui',self)
        self.setWindowIcon(QIcon('./part1/studyPython/set.png'))
        self.setWindowTitle('내 컴퓨터 정보 V0.1') # 이름 설정

        self.refresh.clicked.connect(self.btnrefreshClicked)
        self.initinfo()
        
    def btnrefreshClicked(self):
        self.initinfo()

    def initinfo(self):
        cpu = psutil.cpu_freq()
        cpu_ghz = round(cpu.current / 1000.2)
        self.lblcpu.setText(f'{cpu_ghz:.2f}GHZ')
        core = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        self.lblcore.setText(f'{core} 개 / 논리프로세서 {logical} 개')

        memory = psutil.virtual_memory()
        mem_total = round(memory.total/ 1024**3)
        self.lblmemory.setText(f'{mem_total} GB')

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk.fstype == 'NTFS':
                du = psutil.disk_usage(disk.mountpoint)
                du_total = round(du.total / 1024**3)
                msg = f'{disk.mountpoint} {disk.fstype} - {du_total} GB'
                self.lbldisk.setText(msg)
                break

        in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        in_addr.connect(('www.google.com',443))
        self.lblinnernet.setText(in_addr.getsockname()[0])

        req = requests.get('http://ipconfig.kr')
        out_addr = req.text[req.text.find('<font color=red>')+17:req.text.find('</font><br>')]
        self.lblextranet.setText(out_addr)

        net_stat = psutil.net_io_counters()
        sent = round(net_stat.bytes_sent / 1024**2, 1)
        recv = round(net_stat.bytes_recv / 1024**2, 1)
        self.lblnet.setText(f'송신 - {sent} MB / 수신 - {recv} MB')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())