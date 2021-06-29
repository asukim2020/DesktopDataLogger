import socket
import sys
import threading


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

                if c == 10 or c == '$':
                    tmp = ''.join(self.line)
                    print(tmp)
                    self.line.clear()


            # conn.sendall(reply)
            print(data)

        # came out of loop
        conn.close()
        print("close")


# Test Code
if __name__ == "__main__":
    server = TCPServer()
    server.startServer()
