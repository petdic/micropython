import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import time
from flask_cors import CORS

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)

app.config['MQTT_BROKER_URL'] = '192.168.0.81'
app.config['MQTT_BROKER_PORT'] = 1883

app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)

# ============= SOCKETS ================================
# this will run when the website sends a subscribe event
@socketio.on('subscribe')
def handle_subscribe(json_str):
    print("socket on subscirbe")
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
# ======================================================


# ============= MQTT ===================================
# this will run when the esp32 connects to the broker
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('temp_humidity')

# this will run when a message is recieved, mqtt must be subscribed to the topic
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    t, h = [x for x in data["payload"].split(',')]

    print("=============== Message Recieved: " +
          time.strftime("%H:%M:%S", time.localtime()) + " ===================")
    print("Temperature: " + t)
    print("Humidity: " + h)

    socketio.emit('mqtt_message', data=data)


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
    # print(level, buf)

# ====================================================


if __name__ == '__main__':
    socketio.run(app, host='192.168.0.81', port=5000,
                 use_reloader=False, debug=True)
