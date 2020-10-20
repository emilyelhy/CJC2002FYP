from machine import UART, Pin, Signal
import utime

class Ultrasonic:
    def __init__(self):
        self.Serial2 = UART(2)
        self.Serial2.init(115200, bits=8, parity=None, stop=1)
        self.firstData = ""
        self.secondData = ""
        self.data = bytearray(2)
        self.distance = 0.0
        self.nowTime = 0.0
        self.lastTime = 0.0
        self.deltaTime = 0.0
        self.sumTime = 0.0
        self.t = 0.0
        self.buf = bytearray(2)
        self.trig = Pin(17, Pin.OUT)
        self.echo = Pin(16, Pin.IN)
        self.time = 0.0

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
        utime.sleep_ms(60)
        self.trig.value(0)
        while self.echo.value() != 0:
            if self.getCount(1): self.time = self.time + 1
        # print("time(in ms):", self.time)
        self.distance = (self.time*0.34) / 2
        print("distance(in mm):", self.distance)

        # self.Serial2.write(b'\x55')
        # while True:
        #     if self.getCount(1000): break
        #     if self.Serial2.any():
        #         self.Serial2.readinto(self.data, 2)
        #         print("1st byte received:", self.data[0])
        #         print("2nd byte received:", self.data[1])
        #     break
            
            # self.firstData = self.Serial2.read(1)
            # print("1st byte received:", self.firstData[0])
            # while True:
            #     if self.Serial2.any():
            #         self.secondData = self.Serial2.read(1)
            #         print("2nd byte received:", self.secondData[0])
            #         break
            # self.distance = self.firstData[0]*256 + self.secondData[0]
            # print("Distance(mm):", self.distance)
                # int.from_bytes(self.data, byteorder='big')
                # print("decoded:", self.data)


if __name__ == "__main__":
    led = Pin(2, Pin.OUT)
    led.off()
    print("Start receiving")
    while True:
        Ultrasonic().loop()