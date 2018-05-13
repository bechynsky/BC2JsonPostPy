import time
import requests
import json
import configparser
import paho.mqtt.client as mqtt


# creta config.ini file, this file is ignored by git
# if URL contains % use %%
# [DEFAULT]
# URL = https://...
# COM = /dev/tty...
# MQTT = localhost
configuration = configparser.ConfigParser()
configuration.read('config.ini')

# read configuration
URL = configuration['DEFAULT']['URL']
MQTT_SERVER = configuration['DEFAULT']['MQTT_SERVER']
MQTT_PORT = int(configuration['DEFAULT']['MQTT_PORT'])

# Example of headers
HEADER = {'Content-Type': 'application/json'}


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topicParts = msg.topic.split('/')
    
    if len(topicParts) != 5:
        return

    # create payload, it will be converted to JSON
    payload = {'device': topicParts[1],
                'sensor': topicParts[2], 
                'sensorInfo': topicParts[3], 
                'measurement': topicParts[4],
                'value': msg.payload,
                'time': time.strftime("%Y-%m-%d %H:%M:%S")}

    print(payload)  

    # send payload, payload is converted to JSON
    r = requests.post(URL, json = payload, headers=HEADER)
    # response code
    print(r.status_code)
    


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("END")
