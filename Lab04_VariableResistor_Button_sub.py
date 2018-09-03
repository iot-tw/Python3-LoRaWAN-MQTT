#! /usr/bin/python
# -*- coding: utf8 -*-
# LAB03中 用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。仍保留
# 增加一個按鈕，連續按壓5秒以上，發送一個 button down 事件通知。
__author__ = "Marty Chao"
__version__ = "1.0.3"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Changelog 1.0.3 移除credentials 機制,增加私網公網MQTT 抓取機制
#           增加能從自建MQTT broker 上頭取資料

import paho.mqtt.client as mqtt
import json
LAZY = "mqtt.lazyengineers.com"
SELF = "192.168.88.198"
HostName = LAZY
PortNumber = 1883
Topic = "GIOT-GW/UL/#"
# 只抓取所需要的模組設備,請更改成自己手上的模組MAC
macAddr = "050000c9"
if HostName == LAZY :
    # Topic = "GIOT-GW/UL/1C497B499010"
    # 用+號可以把broker 上頭所有的UL topic 都抓下來
    Topic = "GIOT-GW/UL/+"
    # 如果把 mosqitto.conf 的設定取消 #allow_anonymous false 下面U/P 也不需要了.
    UserName = "lazyengineers"
    Password = "lazyengineers"

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    print(json_data)
    sensor_data = json.loads(json_data)[0]['data']
    # print( sensor_data[0:2])
    # 42 是arduion 端定義 按鈕按下的代碼的 ASCII code 的值
    if sensor_data[0:2] == "42":
        button_status = "Yes"
    else:
        button_status = "No"
    sensor_value = str(int(float(sensor_data.decode("hex")[1:]) / 1023 * 100))
    print('Button Pushed:\033[0;31;40m' + button_status + '\033[0m value: \033[0;32;40m' + sensor_value + '%\033[0m Time: ' + json.loads(
        json_data)[0]['time'] + " GWID:" + json.loads(json_data)[0]['gwid'] + " SNR:" + str(json.loads(json_data)[0]['snr']))
    # hum_value = sensor_value.split("/")[0]
    # temp_value = sensor_value.split("/")[1]
    # print("Hum:"+hum_value+", Temp:"+temp_value)


client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)

client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
