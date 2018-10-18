#! /usr/bin/python3
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
import Adafruit_CharLCD as LCD
import paho.mqtt.client as mqtt
import json
LAZY = "mqtt.lazyengineers.com"
SELF = "192.168.88.198"
HostName = LAZY
PortNumber = 1883
Topic = "GIOT-GW/UL/+"
UserName = "lazyengineers"
Password = "lazyengineers"
# 只抓取所需要的模組設備,請更改成自己手上的模組MAC
macAddr = "050000c9"
# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload[0]
    # print(json_data)
    sensor_data = json.loads(json_data)['data']
    # print( sensor_data[0:2])
    if sensor_data[0:2] == "42":
        button_status = "Yes"
    else:
        button_status = "No"
    sensor_value = str(int(float(sensor_data.decode("hex")[1:])/1023*100))
    print('Button Pushed:\033[0;31;40m' + button_status + '\033[0m value: \033[0;32;40m' + sensor_value + '%\033[0m Time: ' + json.loads(json_data)['time'] + " GWIP:" + json.loads(json_data)['gwip'] + " SNR:" + str(json.loads(json_data)['snr']))
    # lcd.clear()
    lcd.message("R-Value:" + sensor_value + "%\n")
    lcd.message("Button :" + button_status + "\n")
    # hum_value = sensor_value.split("/")[0]
    # temp_value = sensor_value.split("/")[1]
    # print("Hum:"+hum_value+", Temp:"+temp_value)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)

client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
