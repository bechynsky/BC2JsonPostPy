import time
import requests
import json
import configparser
import paho.mqtt.client as mqtt


# creta config.ini file
# if URL contains % use %%
# [DEFAULT]
# URL = https://...
# COM = /dev/tty...
# MQTT = localhost
configuration = configparser.ConfigParser()
configuration.read('config.ini')

URL = configuration['DEFAULT']['URL']
MQTT_SERVER = configuration['DEFAULT']['MQTT_SERVR']
MQTT_PORT = configuration['DEFAULT']['MQTT_PORT']

# This is reqired by Request trigger
HEADER = {'Content-Type': 'application/json'}


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topicParts = msg.topic.split('/')
    
    if len(topicParts) != 4:
        return

    # create payload
    payload = {'device': topicParts[0],
                'sensor': topicParts[1], 
                'sensorInfo': topicParts[2], 
                'measurement': topicParts[3],
                'value': msg.payload,
                'time': time.strftime("%Y-%m-%d %H:%M:%S")}

    print(payload)  

    # send payload, payload is converted to JSON
    r = requests.post(URL, json = payload, headers=HEADER)
    # proper return code is 202 (Accepted), https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#2xx_Success
    print(r.status_code)
    


client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()
