#! /usr/bin/python3
# -*- coding: utf8 -*-
# dummy 就是不用模組也可驗證MQTT 連線的狀況，範例裏的 IP, account 是會固定吐出MQTT 資訊的。
__author__ = "Marty Chao"
__version__ = "2.0.2"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change Log 1.0.3 , support paho-mqtt v1.2
# Change Log 1.0.4 , 優化顯示訊息
# Change Log 2.0.1 , Python 3 version
# Change Log 2.0.2 , format for PEP8

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("You python need isntal paho-mqtt module")
    print("cmd:pip3 install paho-mqtt")
    exit()
import json
HostName = "mqtt.lazyengineers.com"
PortNumber = 1883
Topic = "GIOT-GW/#"
UserName = "lazyengineers"
Password = "lazyengineers"
# 放上要抓取的MacAddr 如果不改 就是全抓
MacAddr = "00000000"

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
#   print(json_data)
    sensor_data = json.loads(json_data)[0]['data']
    sensor_macaddr = json.loads(json_data)[0]['macAddr']
    sensor_time = json.loads(json_data)[0]['time']
    date_value = sensor_time.split("T")[0]
    time_value = sensor_time.split("T")[1]
    if (sensor_macaddr == MacAddr) or (MacAddr == "00000000"):
        print("Topic:" + msg.topic)
        print(json_data)
        print(
            "date:" + date_value
            + ", time:" + time_value
            + " AT+DTX payload:" + sensor_data)


client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)

# client.connect(HostName, PortNumber, 60)
client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
