import socket
import sys
import threading

from python.serial.SerialManager import SerialManager
from python.serial.TimeUtil import TimeUtil


class TCPServer:

    def __init__(self):
        self.host = ''  # Symbolic name meaning all available interfaces
        self.port = 8888  # Arbitrary non-privileged port
        self.line = []

    def startServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        # Bind socket to local host and port
        try:
            serverSocket.bind((self.host, self.port))
            print('Socket bind complete')
        except serverSocket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        thread = threading.Thread(target=self.serverThread, args=[serverSocket])
        thread.start()

    def serverThread(self, serverSocket):
        # Start listening on socket
        serverSocket.listen(10)
        print('Socket now listening')

        # now keep talking with the client
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = serverSocket.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))

            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            thread = threading.Thread(target=self.clientThread, args=[conn])
            thread.start()

        s.close()

    # Function for handling connections. This will be used to create threads
    def clientThread(self, conn):
        # Sending message to connected client
        conn.send(b'Welcome to the server. Type something and hit enter\n')  # send only takes string

        # infinite loop so that function do not terminate and thread do not end.
        while True:

            # Receiving from client
            data = conn.recv(1024)
            if not data:
                break

            for c in data:
                self.line.append(chr(c))
                print(chr(c))

                # if c == 10 or c == '$':
                if chr(c) == '$':
                    tmp = ''.join(self.line)
                    self.line.clear()
                    print("$ 발견: %s" % tmp)

                    if '*' not in tmp:
                        print('처리 불가: %s' % tmp)
                        continue

                    idx = tmp.find('*')
                    tmp = tmp[idx:]

                    if '*RS' in tmp:
                        instance = SerialManager.instance
                        instance.slopeRequestSec = 10
                        instance.createSlopeRequestFile()
                        tmp = tmp.replace('*RS', '')
                        tmp = tmp.replace('$', '')
                        tmp = tmp.replace('_', '')
                        try:
                            sec = int(tmp)
                            instance.slopeRequestSec = sec
                        except Exception as e:
                            print(e)

                        print('createSlopeRequestFile()')
                    elif '*RA' in tmp:
                        instance = SerialManager.instance
                        instance.accelRequestSec = 10
                        instance.createAccelRequestFile()
                        tmp = tmp.replace('*RA', '')
                        tmp = tmp.replace('$', '')
                        tmp = tmp.replace('_', '')
                        try:
                            sec = int(tmp)
                            instance.accelRequestSec = sec
                        except Exception as e:
                            print(e)

                        print('createAccelRequestFile()')
                    elif '*A' in tmp:
                        tmp = tmp.replace('*A', '')
                        tmp = tmp.replace('$', '')
                        list = tmp.split('_')
                        try:
                            if len(list) == 3:
                                SerialManager.accelMeasureHour = int(list[0])
                                SerialManager.accelMeasureMin = int(list[1])
                                SerialManager.accelIntervalPerSec = int(list[2])
                                SerialManager.saveSettingData()
                        except Exception as e:
                            print(e)

                        print('가속도 센서 시간 지정')
                    elif '*S' in tmp:
                        tmp = tmp.replace('*S', '')
                        tmp = tmp.replace('$', '')
                        list = tmp.split('_')
                        try:
                            if len(list) == 3:
                                SerialManager.slopeMeasureHour = int(list[0])
                                SerialManager.slopeMeasureMin = int(list[1])
                                SerialManager.slopeIntervalPerSec = int(list[2])
                                SerialManager.saveSettingData()
                        except Exception as e:
                            print(e)
                        print('경사 센서 시간 지정')
                    elif '*T' in tmp:
                        tmp = tmp.replace('*T', '')
                        tmp = tmp.replace('$', '')
                        list = tmp.split('_')
                        try:
                            if len(list) == 2:
                                SerialManager.abnormalXMax = 3.5
                                SerialManager.abnormalXMin = 1
                                SerialManager.abnormalXMin = int(list[0])
                                SerialManager.abnormalXMax = int(list[1])
                                SerialManager.saveSettingData()
                        except Exception as e:
                            print(e)
                        print('트리거 레벨 설정')
                    elif '*C' in tmp:
                        SerialManager.abnormalXMax = 0
                        tmp = tmp.replace('*C', '')
                        tmp = tmp.replace('$', '')
                        list = tmp.split('_')
                        try:
                            if len(list) == 2:
                                TimeUtil.standardHour = 0
                                TimeUtil.standardMin = 0
                                TimeUtil.standardHour = int(list[0])
                                TimeUtil.standardMin = int(list[1])
                                TimeUtil.saveSettingData()
                        except Exception as e:
                            print(e)
                        print('기준시 설정')
                    else:
                        print('처리 불가: %s' % tmp)

            # conn.sendall(reply)
            # print(data)

        # came out of loop
        conn.close()
        print("close")


# Test Code
if __name__ == "__main__":
    server = TCPServer()
    server.startServer()

    # tmp = "*A4_5_100$"
    # tmp = tmp.replace('*A', '')
    # tmp = tmp.replace('$', '')
    # list = tmp.split('_')
    # print(list)
    # print(list[0])
    # print(list[1])
    # print(list[2])
