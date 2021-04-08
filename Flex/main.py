import machine
from time import sleep
import usocket
import network
import sys

HOST = '192.168.118.134'
PORT = 8964
SSID = 'Mars'
PSWD = '12345678'

class Flex:
    def __init__(self):
        # serial write
        self.Serial2 = machine.UART(2)
        self.Serial2.init(115200, bits=8, parity=None, stop=1)
        # # flex sensor
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
        while not self.sta.isconnected():
            self.sta.connect(SSID, PSWD)
            sleep(3)
        if self.sta.isconnected():
            print("Connected to Wifi with SSID", SSID)
            # server connection
            # work on my pc
            # self.sd = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, 0)
            # mars u try this
            self.sd = usocket.socket(usocket.AF_INET6, usocket.SOCK_STREAM, 0)
            if(self.sd):
                try:
                    self.sd.connect(usocket.getaddrinfo(HOST, PORT)[0][-1])
                    print("Connected to server with HOST", HOST, "and PORT", PORT)
                except Exception as e:
                    print("Fail to connect to server with HOST", HOST, "and PORT", PORT)
                    print(e)
                    sys.exit()
        else:
            # actually will not enter this lol
            print("Fail to connect to Wifi with SSID", SSID)
            sys.exit()

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
        f.loop()
