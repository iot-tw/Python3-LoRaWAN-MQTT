#! /usr/bin/python
# -*- coding: utf8 -*-
# 這是用可變電阻當成 偵測器的輸入，轉動可變電阻可得到 0-100% 的數值。
# LAB02 的代碼仍保留 comment 起來。
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
# 只抓取所需要的模組設備
filter = 0 # if filter is 0, show all module
macAddr = "050000c9"
if HostName == LAZY:
    # Topic = "GIOT-GW/UL/1C497B499010"
    # 用+號可以把broker 上頭所有的UL topic 都抓下來
    Topic = "GIOT-GW/UL/+"
    # 如果把 mosqitto.conf 的設定取消 #allow_anonymous false 下面U/P 也不需要了.
    UserName = "lazyengineers"
    Password = "lazyengineers"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 4:
        print("Please Chect your Username and password")
    elif rc == 0:
        print("Connected,wait for MQTT data")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    # 放弃了的GIOT 云服务
    if HostName == "52.193.146.103":
        json_data = json.loads(msg.payload)
        sensor_time = json_data['recv']
        sensor_gwip = json_data['extra']['gwip']
        sensor_rssi = json_data['extra']['rssi']
    else:
        json_data = json.loads(msg.payload)[0]
        sensor_time = json_data['time']
        sensor_gwip = json_data['gwip']
        sensor_rssi = json_data['rssi']
    print(json_data)
    sensor_data = json_data['data']
    # print sensor_data
    sensor_macAddr = json_data['macAddr'][-8:]
    if sensor_macAddr == macAddr or filter == 0:
        sensor_value = str(int(float(sensor_data.decode("hex"))/1023*100))
        print('macAddr: ' + sensor_macAddr  + ' value: ' + sensor_value + '% Time: ' + sensor_time + " GWIP:" + sensor_gwip + " rssi:" + str(sensor_rssi))


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
