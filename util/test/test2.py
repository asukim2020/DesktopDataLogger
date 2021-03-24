import asyncio
import signal
import threading

import serial
import wx

from util.test import serial_test

line = []  # 라인 단위로 데이터 가져올 리스트 변수

port = 'COM1'  # 시리얼 포트
baud = 38400  # 시리얼 보드레이트(통신속도)

exitThread = False  # 쓰레드 종료용 변수


# 쓰레드 종료용 시그널 함수
def handler(signum, frame):
    exitThread = True


# 데이터 처리할 함수
def parsing_data(data):
    # 리스트 구조로 들어 왔기 때문에
    # 작업하기 편하게 스트링으로 합침
    tmp = ''.join(data)

    # 출력!
    print(tmp)


# 본 쓰레드
def readThread(ser):
    global line
    global exitThread

    # 쓰레드 종료될때까지 계속 돌림
    while not exitThread:
        # 데이터가 있있다면
        for c in ser.read():
            # line 변수에 차곡차곡 추가하여 넣는다.
            line.append(chr(c))

            if c == 10:  # 라인의 끝을 만나면..
                # 데이터 처리 함수로 호출
                parsing_data(line)

                # line 변수 초기화
                del line[:]


class CalcFrame(serial_test.MyFrame4):
    def __init__(self, parent):
        serial_test.MyFrame4.__init__(self, parent)
        self.ser = None

    def clickStart(self, event):
        # 시리얼 열기
        self.ser = serial.Serial(port, baud, timeout=0)
        self.ser.write(b"*S$")
        # 시리얼 읽을 쓰레드 생성
        thread = threading.Thread(target=readThread, args=(self.ser,))

        # 시작!
        thread.start()

    def clickEnd(self, event):
        print("clickEnd")

        global exitThread
        exitThread = True
        if self.ser is not None:
            self.ser.close()

        self.ser = None


if __name__ == "__main__":
    app = wx.App(False)
    frame = CalcFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()
