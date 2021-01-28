import socket

# HOST = socket.gethostname()
HOST = '172.20.10.4'
PORT = 8964
print(HOST, PORT)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sd:
while True:
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
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
            print("Received and Sent: ", data.decode('utf-8'))
