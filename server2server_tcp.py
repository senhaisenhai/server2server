from multiprocessing import Process
import socket
import os

HOST = ''                 # Symbolic name meaning all available interfaces
HOST2 = ''
PORT = 9002
PORT2 = 9000               # Arbitrary non-privileged port

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((HOST2, PORT2))
s2.listen(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()    
print('Connected by esp8266', addr)

conn2, addr2 = s2.accept()    
print('Connected by openpilot', addr)


def process1():
    while True:    
        data2 = conn2.recv(1024)
#        print("data from openpilot:", data2)
        conn.sendall(data2)
 
def process2():
    while True:
        data = conn.recv(1024)
#        print("data from esp8266", data)
        conn2.sendall(data)

if __name__ == '__main__':
    p1 = Process(target=process1)
    p2 = Process(target=process2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


