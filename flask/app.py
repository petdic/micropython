from flask import Flask
from flask_mqtt import Mqtt
import time

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '192.168.0.81'
app.config['MQTT_BROKER_PORT'] = 1883
#app.config['MQTT_USERNAME'] = 'user'
#app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)


@app.route('/')
def index():
    return "Test"


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('temp_humidity')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("=============== Message Recieved: " +
          time.strftime("%H:%M:%S", time.gmtime()) + " ===================")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    t, h = [x for x in data["payload"].split(',')]
    print("Temperature: " + t)
    print("Humidity: " + h)


if __name__ == '__main__':
    app.run(host='192.168.0.81', port=5000)
