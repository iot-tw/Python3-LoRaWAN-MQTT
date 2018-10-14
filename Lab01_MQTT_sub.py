#! /usr/bin/python
# -*- coding: utf8 -*-
# 搭配 LAB01 Arduino 的上傳資料 AT_DTX Raw Data
__author__ = "Marty Chao"
__version__ = "1.0.3"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.2, support paho-mqtt 1.2
# Change log 1.0.3, 去掉credentials 機制
# Change Log 1.0.4, clean useless comment and format for PEP8

import paho.mqtt.client as mqtt
HostName = "mqtt.lazyengineers.com"
PortNumber = 1883
Topic = "GIOT-GW/#"
UserName = "lazyengineers"
Password = "lazyengineers"
macAddr = "05000095"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    json_data = msg.payload
    print(json_data)


client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)
# 這裏第三個參數可以調整，每個多少時間檢查MQTT 連線狀態，通常60秒已經算短的了，爲了實驗，可以用60秒。
# 2-5分鐘都算合理，google 的 GCM 都28分鐘檢查一次了，在實際量產部署時，要重新考慮這個值，頻寬及Server Load 不是免費啊。
client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
