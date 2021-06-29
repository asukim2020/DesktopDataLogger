import socket
import sys
import threading

from python.serial.SerialManager import SerialManager


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

                    idx = tmp.find('*')
                    tmp = tmp[idx:]
                    print("$ 발견: %s" % tmp)

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

            # conn.sendall(reply)
            # print(data)

        # came out of loop
        conn.close()
        print("close")


# Test Code
if __name__ == "__main__":
    server = TCPServer()
    server.startServer()
