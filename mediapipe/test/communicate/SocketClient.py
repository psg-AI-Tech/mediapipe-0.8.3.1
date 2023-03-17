import socket
import time
class SocketClient():
    def __init__(self,ip,port) -> None:
        self.ip=ip
        self.port=port
        self.sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # TODO 一直连接直到连接上
    
    def connectUntil(self):
        while True:
            try: 
                if self.connect():  
                    print("connect success! ",(self.ip,self.port))
                    self.send("I'm client1")
                    break;
            except:
                print("connect failed! try again",(self.ip,self.port))
                time.sleep(0.5)
                continue;


        
    def connect(self):
        status =self.sockfd.connect((self.ip,self.port))
        return status
    def send(self,data):
        self.sockfd.send(bytes(data.encode('utf-8')))
    def recv(self):
        return self.sockfd.recv(2048)





import json
import params

# IP ="192.168.2.106"
# PORT =8080
IP =params.host
PORT =params.PORT

def testClient():
    client =SocketClient(IP ,PORT)
    client.connect()
    while True:
        try:
            msg =client.recv()
            msg=msg.decode('utf-8')
            recvmsg=json.loads(msg)

            keylist =recvmsg.keys()
            print("recv msg: ",type(recvmsg),len(keylist))
            print("key list",keylist)
            # time.sleep(0.1)
        except:
            time.sleep(1)
            print("rec error")
            continue;
def main():

    testClient()
    pass

if __name__ =="__main__":
    main()