from time import sleep
import time
from umqtt.simple import MQTTClient
import ubinascii
from machine import Pin
import machine
from dht import DHT11
import network

connected = False


def wifi_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    results = station.scan()
    global connected
    if results and not connected:
        for x in results:
            wifi = x[0]
            if wifi == b'Dicey 2' and not connected:
                print("Connecting to Dicey 2...")
                station.connect("Dicey 2", "84735peter")
                connected = True
            if wifi == b'Dicey' and not connected:
                print("Connecting to Dicey...")
                station.connect("Dicey", "Peter84735")
                connected = True
    else:
        print("No wireless devices detected...")
    sleep(5)


def main():
    while True:
        if connected == False:
            print("Connecting to Wifi...")
            wifi_connect()
            print("Connected to Wifi")
        else:
            try:
                print("Setting up Client...")
                broker_address = '192.168.0.81'
                client_id = 'esp32_{}'.format(
                    ubinascii.hexlify(machine.unique_id()))
                topic = b'temp_humidity'
                client = MQTTClient(client_id, broker_address)
                client.set_last_will(topic, b'dead')
                print("Connecting Client...")
                client_connect = False
                try:
                    client.connect()
                    client_connect = True
                    print("Connected to Broker")
                except:
                    print("Failed to connect the Client")
                    sleep(4)
                sensor = DHT11(Pin(5))
            except:
                print("Failed to setup the Client")

            if client_connect:
                while True:
                    try:
                        clock = time.localtime()

                        print("=============== Topic Published: " +
                              str(clock[3]) + ":" + str(clock[4]) + ":" + str(clock[5]) + " ===================")

                        sensor.measure()
                        t = sensor.temperature()
                        h = sensor.humidity()
                        msg = ('{0},{1}'.format(t, h))
                        try:
                            client.publish(topic, msg)
                            print(msg)
                        except:
                            print("Failed to Publish")
                            break
                    except OSError:
                        print("Failed to read sensor")
                        break
                    sleep(4)


main()
