import machine
from time import sleep
import socket
import network

HOST = '172.20.10.4'
PORT = 8964
SSID = 'Hei Yiu\'s iPhone'
PSWD = '16121998'

class Flex:
    def __init__(self):
        # serial write
        self.Serial2 = machine.UART(2)
        self.Serial2.init(115200, bits=8, parity=None, stop=1)
        # # flex sensor
        # self.thumb = machine.ADC(machine.Pin(32))
        # self.index = machine.ADC(machine.Pin(35))
        # self.middle = machine.ADC(machine.Pin(34))
        # self.ring = machine.ADC(machine.Pin(36))
        # self.little = machine.ADC(machine.Pin(39))
        self.thumb = machine.ADC(machine.Pin(39))
        self.index = machine.ADC(machine.Pin(36))
        self.middle = machine.ADC(machine.Pin(34))
        self.ring = machine.ADC(machine.Pin(35))
        self.little = machine.ADC(machine.Pin(32))
        # flex const
        self.max = [4095, 1420, 1420, 1350, 4095]
        self.straight = [1700, 700, 700, 700, 1700]
        # flex value
        self.value = [0, 0, 0, 0, 0]
        self.range = [0, 0, 0, 0, 0]
        # network connection
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)
        print(self.sta.scan())
        # while not self.sta.isconnected():
        #     self.sta.connect(SSID, PSWD)
        print("Connected to Wifi with SSID", SSID)
        # server connection
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if(self.sd):
            self.sd.connect((HOST, PORT))

    def loop(self):
        self.value[0] = self.thumb.read()
        self.value[1] = self.index.read()
        self.value[2] = self.middle.read()
        self.value[3] = self.ring.read()
        self.value[4] = self.little.read()
        # self.value[0] = self.value[4] = 0
        for i in range(5):
            if self.value[i] < self.straight[i]:
                self.value[i] = self.straight[i]
            elif self.value[i] >self.max[i]:
                self.value[i] = self.max[i]
            self.value[i] = (self.value[i] - self.straight[i]) / (self.max[i] - self.straight[i])
            self.value[i] = int(float("{:.2f}".format(self.value[i])) * 100)
            # if self.value[i] < 0.4:
            #     self.range[i] = 0
            # else: self.range[i] = 1
        command = "F" + str(self.value)
        print(command)
        self.sd.sendall(command.encode('utf-8'))
        # self.Serial2.write(command)
        sleep(0.05)

if __name__ == "__main__":
    f = Flex()
    print("Start Receiving")
    while True:        
        with self.sd:
            f.loop()
