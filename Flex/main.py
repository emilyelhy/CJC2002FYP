import machine
from time import sleep

class Flex:
    def __init__(self):
        # serial write
        self.Serial2 = machine.UART(2)
        self.Serial2.init(115200, bits=8, parity=None, stop=1)
        # flex sensor
        self.thumb = machine.ADC(machine.Pin(39))
        # self.index = 
        # self.middle = 
        # self.ring = 
        # self.little = 
        # flex const
        self.min = 1000
        self.max = 4095
        self.straight = 1500
        # flex value
        self.value = [0, 0, 0, 0, 0]

    def loop(self):
        self.value[0] = self.thumb.read()
        # self.value[1] = self.index.read()
        # self.value[2] = self.middle.read()
        # self.value[3] = self.ring.read()
        # self.value[4] = self.little.read()
        self.value[1] = self.value[2] = self.value[3] = self.value[4] = 0
        for i in range(5):
            if self.value[i] < self.straight:
                self.value[i] = self.straight
            elif self.value[i] >self.max:
                self.value[i] = self.max
            self.value[i] = (self.value[i] - self.straight) / (self.max - self.straight)
            self.value[i] = "{:.2f}".format(self.value[i])
        command = "F" + str(self.value)
        print(command)
        self.Serial2.write(command)
        sleep(0.05)

if __name__ == "__main__":
    f = Flex()
    print("Start Receiving")
    while True:
        f.loop()

# test = ADC(Pin(39))
# min = 1000
# straight = 1500
# max = 4095

# while True:
#     value = test.read()
#     if value < straight:
#         value = straight
#     elif value > max:
#         value = max
#     value = (value - straight) / (max - straight)
#     value = "{:.2f}".format(value)
#     print("[F]", value)
#     sleep(0.05)