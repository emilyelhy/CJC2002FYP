import socket

HOST = socket.gethostname()
# HOST = '192.168.xx.yy'
PORT = 8964

with socket.socket(AF_INET, SOCK_STREAM, 0) as sd:
    sd.bind((HOST, PORT))
    sd.listen(1)
    conn, addr = sd.accept()
    with conn:
        print("Connected by device with ip", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)