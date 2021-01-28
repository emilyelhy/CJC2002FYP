import socket

# HOST = socket.gethostname()
HOST = '192.168.254.84'
PORT = 8964
print(HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sd:
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
