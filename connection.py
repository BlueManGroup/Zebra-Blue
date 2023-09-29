import socket
import requests
import time

class Connection():
    def __init__(self, q=None):
        self.q = q
        self.host = '130.225.39.30'
        self.port = 8080

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        print("connection established.....")
        while True:
            time.sleep(2)
            print("connection.py queue is empty:", self.q.empty())
            while not self.q.empty():
                packet = self.q.get()
                # You can serialize the packet in various ways, as simple bytes for instance
                sock.send(packet.encode())
            
            