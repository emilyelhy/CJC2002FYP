import socket

# HOST = '192.168.x.x'
PORT = 8964

with socket.socket(AF_INET, SOCK_STREAM, 0) as sd:
    sd.connect((HOST, PORT))
    sendData = 'ABCDEFGH'.encode('utf-8')
    sd.sendall(sendData)
    recvData = sd.recv(1024)
    recvData = recvData.decode('utf-8')
    print("Received: ", recvData)