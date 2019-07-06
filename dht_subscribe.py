import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print('Connected with result code {0}'.format(rc))
    client.subscribe('temp_humidity')


def on_message(client, userdata, msg):
    t, h = [x for x in msg.payload.decode("utf-8").split(',')]
    print('Temperature: {0} \nHumidity: {1}'.format(t, h))
    print('==============================================')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

client.loop_forever()
