from machine import Pin, ADC
from time import sleep

test = ADC(Pin(36))

while True:
    value = test.read()
    print("[F]", value)
    sleep(0.05)