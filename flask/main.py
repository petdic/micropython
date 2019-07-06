import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
# from flask_bootstrap import Bootstrap
import time
import database_handler as db
from flask_cors import CORS

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
# app.config['SECRET'] = 'my secret key'
# app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.0.81'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = ''
# app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
# app.config['SERVER_NAME'] = 'localhost:5000'

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
# bootstrap = Bootstrap(app)

send_counter = 0
web = False


@app.route('/getTemperatures')
def getTemperatures():
    temperatures = db.read_temperature()
    return temperatures


@app.route('/getHumiditys')
def getHumiditys():
    humiditys = db.read_humidity()
    return humiditys


# =============== SOCKETS =============================
# @socketio.on('publish')
# def handle_publish(json_str):
#    data = json.loads(json_str)
#    mqtt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    global web
    web = True
    print("socket on subscirbe")
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])
    # mqtt.subscribe("temp_humidity")


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    global web
    web = False
# ======================================================


# ============= MQTT ===================================
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    global web
    if web == False:
        mqtt.subscribe('temp_humidity')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global web
    global send_counter

    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    t, h = [x for x in data["payload"].split(',')]

    print("Only Records Every Hour: " + str(send_counter))

    if data["topic"] == 'temp_humidity'and web == False:
        if send_counter == 900:
            print("=============== Message Recieved: " +
                  time.strftime("%H:%M:%S", time.localtime()) + " ===================")
            print("Temperature: " + t)
            print("Humidity: " + h)
            db.insert_temperature(t)
            db.insert_humidity(h)
            send_counter = 0
        send_counter += 1

    if data["topic"] == 'temp_humidity' and web == True:
        print("=============== Message Sent: " +
              time.strftime("%H:%M:%S", time.localtime()) + " ===================")
        print("Temperature: " + t)
        print("Humidity: " + h)
        socketio.emit('mqtt_message', data=data)

        print(send_counter)
        if send_counter == 900:
            print("=============== Message Recieved: " +
                  time.strftime("%H:%M:%S", time.localtime()) + " ===================")
            print("Temperature: " + t)
            print("Humidity: " + h)
            db.insert_temperature(t)
            db.insert_humidity(h)
            send_counter = 0
        send_counter += 1


# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
    # print(level, buf)

    # ====================================================


if __name__ == '__main__':
    socketio.run(app, host='192.168.0.81', port=5000,
                 use_reloader=False, debug=True)
    # app.run(host='192.168.0.81', port=5000)
