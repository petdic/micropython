# DHT11 when button click, measure and display

from machine import Pin
import dht
from time import sleep

led = Pin(13, Pin.OUT)
button = Pin(25, Pin.IN, Pin.PULL_DOWN)
sensor = dht.DHT11(Pin(5))

try:
    while True:
        led.value(0)
        if button.value() == 0:
            led.value(1)
            sensor.measure()
            print("Temperature: " + str(sensor.temperature()))
            print("Humidity: " + str(sensor.humidity()))
            sleep(0.5)

except KeyboardInterrupt:
    print("\nCtr-C pressed. Cleaning up and exiting...")
