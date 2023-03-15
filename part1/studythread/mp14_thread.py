import threading
import time # 쓰레드를 하면 타임은 꼭 필요하다

# 쓰레드를 상속받는 백그라운드작업 클래스
class BackgroundWorker(threading.Thread):

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = f'{threading.current_thread().name} : {name}'

    def run(self) -> None:
        print(f'BackgroundWorker start : {self._name}')
        time.sleep(2)
        print(f'BackgroundWorker end : {self._name}') 

if __name__ == '__main__':
    print('기본프로세스 시작') # 기본프로세스 == 메인스레드

    for i in range(5):
        name = f'서브 스레드 {i}'
        th = BackgroundWorker(name)
        th.start()

    print('기본프로세스 종료')