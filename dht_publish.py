from time import sleep
from umqtt.simple import MQTTClient
import ubinascii
from machine import Pin
import machine
from dht import DHT11
import network

# connect to network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Dicey 2", "84735peter")

sleep(5)

broker_address = '192.168.0.81'

# client id can be esp32, doesnt need the last bit
client_id = 'esp32_{}'.format(ubinascii.hexlify(machine.unique_id()))
topic = b'temp_humidity'
client = MQTTClient(client_id, broker_address)

# last will is when it dies, this is the last thing that is sent, i think
# basically you can subscribe to the dead topic and get the logs
client.set_last_will(topic, b'dead')

client.connect()
print("connected to broker")

# ignore, this is for my sensor
sensor = DHT11(Pin(5))


while True:
    try:
        # measure sensor
        sensor.measure()

        # store sensor values
        t = sensor.temperature()
        h = sensor.humidity()

        # msg format with data
        msg = ('{0},{1}'.format(t, h))

        # publish message
        client.publish(topic, msg)
        print(msg)
    except OSError:
        print("Failed to read sensor")
    sleep(4)
