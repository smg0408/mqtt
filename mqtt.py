import paho.mqtt.client as mqtt
import RPi.GPIO as g
import time
import json
from time import sleep
g.setmode(g.BCM)
g.setup(14, g.OUT)
def millis():
    return int(round(time.time() * 1000))
def on_connect(client, userdata, flags, rc):
    print("Connected " + str(rc))
    client.subscribe("iot-2/type/Python/id/dev2/cmd/status/fmt/json")
def on_message(client, userdata, msg):
    m = json.loads(msg.payload)
    if m['d']['led'] == 'on':
        g.output(14, g.HIGH)
    else:
        g.output(14, g.LOW)
    print(msg.topic+" " +str(msg.payload))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
pubInt = 3000
lastPub = 0
cnt = 0
evt = json.loads('{"d":{}}')
while True:
    client.loop()
    if millis() - pubInt > lastPub:
        lastPub = millis()
        cnt = cnt + 1
        evt['d']['count'] = cnt
        client.publish("iot-2/type/Python/id/dev2/evt/status/fmt/json", json.dumps(evt))
