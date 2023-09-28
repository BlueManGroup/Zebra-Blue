import socket
import requests
from queue import Queue

if __name__ == '__main__':
    host = "130.225.39.30"
    port = "8080"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

# Function to send packets to the server
while not packet.queue.empty():
    packet = packet.queue.get()
    # You can serialize the packet in various ways, as simple bytes for instance
    response = requests.post(host, data=bytes(packet))