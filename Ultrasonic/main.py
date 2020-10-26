from machine import UART, Pin, Signal
import machine
import utime

class Ultrasonic:
    def __init__(self):
        self.trig = Pin(17, Pin.OUT)
        self.echo = Pin(16, Pin.IN)
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
        utime.sleep_ms(60)
        self.trig.value(0)
        if self.getCount(50):                 # run per 50ms
            self.time = machine.time_pulse_us(self.echo, 1)
        if self.time > 0:
            self.distance = (self.time*0.34) / 2
        else:
            self.distance = 0.0
        print("distance(in mm):", self.distance)
        self.time = 0.0
        self.distance = 0.0

if __name__ == "__main__":
    led = Pin(2, Pin.OUT)
    led.off()
    print("Start receiving")
    while True:
        Ultrasonic().loop()