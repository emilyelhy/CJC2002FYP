import socket

HOST = '192.168.118.122'
PORT = 8964

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sd:
    sd.connect((HOST, PORT))
    while True:
    	sendData = 'ABCDEFGH'.encode('utf-8')
    	sd.sendall(sendData)