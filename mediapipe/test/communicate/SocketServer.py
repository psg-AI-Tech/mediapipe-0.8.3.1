#!/usr/bin/env python3
import socket
import time
import threading
import sys
sys.path.append("../")

from communicate.params import host,PORT, LINE_NUM

class SocketServer():
    def __init__(self,port) -> None:
        self.sockfd =socket.socket()
        # host =socket.gethostbyname("localhost")
        self.port =port
        self.sockfd.bind((host,port))
        self.sockfd.listen(LINE_NUM)

    def accept(self):
        self.clientConnection,addr=self.sockfd.accept()
        print("连接地址： ",addr)
        # self.clientConnection.send(str.encode("received"))


    def send(self,data):
        try:
            self.clientConnection.send(data)
            return True
        except:
            return False




import json
def serverTest():
    socketserver= SocketServer(PORT)
    dic ={"key01": 123,"key02":456}
    while True:
        socketserver.accept() 
        while True:
            if not socketserver.send(json.dumps(dic).encode("utf-8")):
                # TODO 连续n次发送失败则断开
                time.sleep(1)
                break
            time.sleep(0.1)
        socketserver.clientConnection.close()
    self.sockfd.close()
    pass



def main():
    import json

    serverTest()
    pass

if __name__ =="__main__":
    main()