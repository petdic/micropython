# Blinking LED for Pin13
from machine import Pin
from time import sleep


def main():
    led = Pin(13, Pin.OUT)

    try:
        while(True):
            led.value(not led.value())
            sleep(0.5)
    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Cleaning up and exiting...")
    finally:
        led.value(0)


main()
