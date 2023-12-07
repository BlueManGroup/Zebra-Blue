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
                sock.send(packet.encode())
                # TODO: PACKETS ARE SENT TOO QUCIKLY FOR THE RECEIVER TO BE ABLE TO DISTINGUISH THEM AS SEPARATE PACKETS
                # THIS MEANS THAT PACKETS ARE CONCATENATED WHEN RECEIVED. 
                # MIGHT BE SOLVED WHEN ANOMALY DETECTION ARE THE ONLY PACKETS SENT, BUT SET SOME HARD LIMIT LIKE SLEEP 0.5
            
            
