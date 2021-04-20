import socket

HOST = '192.168.118.122'
PORT = 6000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sd:
    sd.connect((HOST, PORT))
    while True:
	    recvData = sd.recv(1024)
	    recvData = recvData.decode('utf-8')
	    print("Received: ", recvData)
