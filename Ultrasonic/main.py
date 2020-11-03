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
        # below use for counting time interval
        self.nowTime = 0.0
        self.sumTime = 0.0
        self.deltaTime = 0.0
        self.lastTime = 0.0

    def getDeltaTime(self):
        self.nowTime = utime.ticks_ms()
        self.deltaTime = self.nowTime - self.lastTime
        self.lastTime = self.nowTime
        return self.deltaTime

    def getCount(self, interval):
        self.sumTime += self.getDeltaTime()
        if self.sumTime >= interval:
            self.sumTime = 0
            return True
        else:
            return False

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
        self.distance = "{:.2f}".format(self.distance)
        command = "U" + str(self.distance)
        print(command)
        self.Serial2.write(command)
        self.time = 0.0
        self.distance = 0.0

if __name__ == "__main__":
    # ultrasonic sensor ranges from 20mm to 4500mm
    print("Start receiving")
    while True:
        Ultrasonic().loop()
