import machine
import utime

class Ultrasonic:
    def __init__(self):
        # serial write
        self.Serial2 = machine.UART(2)
        self.Serial2.init(115200, bits=8, parity=None, stop=1)
        # ultrasonic sensor
        self.trig = machine.Pin(17, machine.Pin.OUT)
        self.echo = machine.Pin(16, machine.Pin.IN)
        self.time = 0.0
        self.distance = 0.0
        self.range = 0
        # below use for counting time interval
        self.nowTime = 0.0
        self.sumTime = 0.0
        self.deltaTime = 0.0
        self.lastTime = 0.0
        # use for average (filter)
        self.array = [0.0 for i in range(5)]

    # didn't use
    def getDeltaTime(self):
        self.nowTime = utime.ticks_ms()
        self.deltaTime = self.nowTime - self.lastTime
        self.lastTime = self.nowTime
        return self.deltaTime

    # didn't use
    def getCount(self, interval):
        self.sumTime += self.getDeltaTime()
        if self.sumTime >= interval:
            self.sumTime = 0
            return True
        else:
            return False

    def addAverage(self, input):
        for i in range(5):
            index = 4 - i
            if index > 0:
                self.array[index] = self.array[index-1]
        self.array[0] = input
        sum = 0.0
        for i in range(5): sum = sum + self.array[i]
        return (sum / 5)

    def determineRange(self, input):
        if input == 0.0:
            return 0
        if input <= 40.0:
            return 1
        if input <= 80.0:
            return 2
        if input <= 120.0:
            return 3
        if input <= 160.0:
            return 4
        if input <= 200.0:
            return 5
        if input <= 240.0:
            return 6
        if input <= 280.0:
            return 7
        if input <= 320.0:
            return 8
        if input <= 360.0:
            return 9
        if input <= 400.0:
            return 10
        if input <= 440.0:
            return 11
        if input <= 480.0:
            return 12
        return 13

    def loop(self):
        self.trig.value(1)
        utime.sleep_ms(50)
        self.trig.value(0)
        self.time = machine.time_pulse_us(self.echo, 1)
        if self.time > 0 and self.time < 26471:         # becoz sensor ranges from 20mm-4500mm
            self.distance = (self.time*0.34) / 2
        else:
            self.distance = 0.0
        # print("distance(in mm):", self.distance)
        self.distance = self.addAverage(self.distance)
        # self.distance = "{:.2f}".format(self.distance)
        self.distance = int(self.distance)
        # self.range = self.determineRange(self.distance)
        command = "U" + str(self.distance)
        print(command)
        # print(command, "distance: ", "{:.2f}".format(self.distance))
        # self.Serial2.write(command)
        self.time = 0.0
        self.distance = 0.0
        self.range = 0

if __name__ == "__main__":
    # ultrasonic sensor ranges from 20mm to 4500mm
    u = Ultrasonic()
    # print("Start receiving")
    while True:
        u.loop()
