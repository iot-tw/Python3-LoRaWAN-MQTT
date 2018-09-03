#! /usr/bin/python3
# -*- coding: utf8 -*-
# 這是一個樹莓派的範例，用LED 燈號表示溫度高低。
# 需要有Raspberry Pi 才能使用

# sudo pip install paho-mqtt

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
# 處理 giot credentials 設定值
HostName = "mqtt.lazyengineers.com"
PortNumber = 1883
Topic = "GIOT-GW/#"
UserName = "lazyengineers"
Password = "lazyengineers"

LED_R = 17
LED_Y = 27
LED_G = 22


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    # print(json_data)
    sensor_data = json.loads(json_data)['data']
    sensor_value = sensor_data.decode("hex")
    # print('value: ' + sensor_value)
    hum_value = sensor_value.split("/")[0]
    temp_value = sensor_value.split("/")[1]
    print("Hum:"+hum_value+", Temp:"+temp_value)
    iTmp = float(temp_value)
    if iTmp > 30:
        led_on(LED_R)
        led_off(LED_Y)
        led_off(LED_G)
    elif iTmp >= 29 and iTmp <= 30:
        led_off(LED_R)
        led_on(LED_Y)
        led_off(LED_G)
    else:
        led_off(LED_R)
        led_off(LED_Y)
        led_on(LED_G)


def led_on(pin):
    GPIO.output(pin, GPIO.HIGH)


def led_off(pin):
    GPIO.output(pin, GPIO.LOW)


# 鏈接MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(UserName, Password)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_Y, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)

client.connect(HostName, PortNumber, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
GPIO.cleanup()
