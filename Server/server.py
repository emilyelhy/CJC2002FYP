import socket
from _thread import *

def broadcastToAll(CLIENTS, data):
    for client in CLIENTS:
        client.sendall(data)

def newConnection(conn, CLIENTS):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        broadcastToAll(CLIENTS, data)
        print("Received: ", data.decode('utf-8'))
    conn.close()

def main():
    HOST = '192.168.118.122'
    PORT = 8964
    CLIENTS = []
    print(HOST, PORT)
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sd.bind((HOST, PORT))
    print("Bind to HOST", HOST, "with PORT", PORT)
    sd.listen(5)
    while True:
        conn, addr = sd.accept()
        CLIENTS.append(conn)
        print("Connected by device with ip", addr)
        start_new_thread(newConnection, (conn, CLIENTS, ))
    sd.close()

if __name__ == '__main__':
    main()