from machine import Pin, ADC
from time import sleep

test = ADC(Pin(39))
min = 1000
straight = 1500
max = 4095

while True:
    value = test.read()
    if value < straight:
        value = straight
    elif value > max:
        value = max
    value = (value - straight) / (max - straight)
    value = "{:.2f}".format(value)
    print("[F]", value)
    sleep(0.05)