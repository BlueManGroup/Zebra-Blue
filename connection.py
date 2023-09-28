import socket

if __name__ == '__main__':
    host = "130.225.39.30"
    port = "8080"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))