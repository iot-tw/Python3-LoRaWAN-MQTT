#! /usr/bin/python
# -*- coding: utf8 -*-
'''
抓取Local MQTT Broker 的UL 資料,前提是要有自己的GIoT Gateway。
使用台北市府物聯網，宜蘭縣府，新竹市府的PoC 環境是不同格式。
'''
__author__ = "Marty Chao"
__version__ = "1.0.2"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.1, support paho-mqtt 1.2

import paho.mqtt.client as mqtt
import json
import sys
from optparse import OptionParser

usage = "usage: %prog [options] [host]\n\
  host: a MQTT broker IP \n\
  e.g.: '%prog --ip 192.168.1.1' will sub server and print data."

parser = OptionParser(usage)
parser.add_option("-d", "--display-lcd", action="store_true",
                  help="print message to raspberry LCD")
parser.add_option("-l", "--long-detail", action="store_true",
                  help="print detail JSON message")
parser.add_option("-t", "--topic", action="store",
                  dest="topic", default="#",
                  help="provide connection topic")
parser.add_option("-D", "--degree", action="store",
                  dest="degree", default=25,
                  help="relay on off degree")
parser.add_option("-i", "--ip", action="store",
                  dest="host", default="localhost",
                  help="sub from MQTT broker's IP ")
parser.add_option("-u", "--user", action="store",
                  dest="username", default="admin",
                  help="sub from MQTT broker's username ")
parser.add_option("-P", "--pw", action="store",
                  dest="password", default="admin",
                  help="sub from MQTT broker's password ")
parser.add_option("-p", action="store",
                  dest="port", default=1883,
                  help="sub from MQTT broker's Port ")
parser.add_option("-R","--showdownlink", action="store_true",
                  help="If payload is 'FF' print out Downlink Command")
parser.add_option("-r","--downlink", action="store_true",
                  help="If payload is 'something' pub mqtt out Downlink module")
(options, args) = parser.parse_args()
if options.display_lcd:
    import Adafruit_CharLCD as LCD
    lcd = LCD.Adafruit_CharLCDPlate()
if options.downlink:
    import subprocess
print ("MQTT broker is:" + options.host + ":" + str(options.port))
print ("MQTT Topic is:" + options.topic)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    '''
    GIoT Module Json UpLink Example
    GIOT-GW/UL/xxxx [{"channel":923125000, "sf":10,
    "time":"2017-03-13T03:59:29", "gwip":"10.6.1.49",
    "gwid":"0000f835dde7de2e", "repeater":"00000000ffffffff",
    "systype":10, "rssi":-118.0, "snr":0.5, "snr_max":3.8, "snr_min":-4.5,
    "macAddr":"000000000a000158", "data":"015dff017b81ed0736767c",
    "frameCnt":26920, "fport":2}]
    '''
    # client.subscribe(Topic)
    # client.subscribe("GIOT-GW/UL/+")
    # client.subscribe("GIOT-GW/UL/1C497B4321AA")
    client.subscribe("#")
    # GIOT-GW/DL/1C497B499010 [{"macAddr":"0000000004000476","data":"5678","id":"998877ffff0001","extra":{"port":2, "txpara":6}}]
    # GIOT-GW/DL-report/1C497B499010 {"dataId":"16CBD520C19162013CD6436CB330565E", "resp":"2016-11-30T15:02:40Z", "status":-1}


def on_message(client, userdata, msg):
    json_data = msg.payload
    print(json_data)
    # print(msg.topic+" "+str(msg.payload))
    if msg.topic[:11] == "GIOT-GW/DL/":
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        sensor_value = sensor_data.decode("hex")
        sensor_id = json.loads(json_data)[0]['id']
        sensor_txpara = json.loads(json_data)[0]['extra']['txpara']

    elif msg.topic[:11] == "GIOT-GW/UL/":
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        sensor_value = sensor_data.decode("hex")
        gwid_data = json.loads(json_data)[0]['gwid']
        sensor_snr = json.loads(json_data)[0]['snr']
        sensor_rssi = json.loads(json_data)[0]['rssi']
        sensor_count = json.loads(json_data)[0]['frameCnt']
    else:
        # print (msg.topic+" "+str(msg.payload))
        sensor_mac = '0000000000000000'
        sensor_data = '0000000000000000'
    if "0a" == str(sensor_mac)[8:10]:
        sensor_type = 'Asset Tracker'
    elif "04" == str(sensor_mac)[8:10]:
        sensor_type = 'Module Taipei'
    elif "05" == str(sensor_mac)[8:10]:
        sensor_type = 'Module Taiwan'
    elif "00" == str(sensor_mac)[8:10]:
        sensor_type = 'Location Box '
    elif "0d" == str(sensor_mac)[8:10]:
        sensor_type = 'Parking Can  '
    elif "02" == str(sensor_mac)[8:10]:
        sensor_type = 'RS485 tranmit'
    else:
        sensor_type = 'Unknow Module'
    if msg.topic[:11] == 'GIOT-GW/UL/':
        print('Type:' + sensor_type + '\tMac:' + str(sensor_mac)[8:]
              + '\tCount:' + str(sensor_count).rjust(6)
              + '\tSNR:' + str(sensor_snr).rjust(4)
              + '\tRSSI:' + str(sensor_rssi).rjust(4)
              + '\tGWID:' + str(gwid_data).rjust(8))
    elif msg.topic[:11] == 'GIOT-GW/DL/':
        print('Type:' + sensor_type + '\tMac:' + str(sensor_mac)[8:] + '\tMID:' + str(sensor_id) + '\tTXPara:' + str(sensor_txpara))
    elif msg.topic[:17] == 'GIOT-GW/DL-report':
        print('Response:' + msg.topic[18:] + '\tStatus:' + str(json.loads(json_data)['status']) + '\tID:' + json.loads(json_data)['dataId'])
    else:
        print (msg.topic + msg.payload)
    if options.display_lcd:
        lcd.clear()
        lcd.message(str(sensor_mac)[8:]+' C:'+str(sensor_count))
        lcd.message('\nS/R:' + str(sensor_snr) + '/' + str(sensor_rssi))

    # if gwid_data == "00001c497b48dc03" or gwid_data == "00001c497b48dc11":
    if msg.topic[:7] == 'GIOT-GW' and msg.topic[:10] != 'GIOT-GW/DL':
        try:
            #print sensor_data.decode("hex") + str(sensor_mac)[8:].upper()
            if sensor_data.decode("hex") == str(sensor_mac)[8:].upper() and options.showdownlink:
                print('\x1b[6;30;42m' + './pub_dl_local.py -i ' + options.host +' -m '+ str(sensor_mac)[8:]+ ' -g ' + str(gwid_data) + ' -c A' +'\x1b[0m')
                lora_restart = raw_input('Stop MQTT subscribe?[Y/n]:') or "y"
                if lora_restart == 'Y' or lora_restart == 'y':
                    sys.exit()
            if sensor_data == "3035303130333135" and options.downlink:
                print("pub downlink to local broker")
                print("gwid:" + str(gwid_data))
                subprocess.Popen(["./pub_dl_local.py", "-i", options.host, "-m", str(sensor_mac)[8:], "-g", str(gwid_data), "-c", "c"])
            if str(sensor_mac)[8:] == "05010175" and options.downlink:
                print("pub downlink to control something , turn on LED")
                if sensor_data[0:2] == "01":
                    meter_type = "CO2+RHT"
                elif sensor_data[0:2] == "10":
                    meter_type = "CO+RHT"
                elif sensor_data[0:2] == "11":
                    meter_type = "PM2.5+RHT"
                print(sensor_data[2:6])
                meter_temp = float(int(sensor_data[2:6], 16))/100
                meter_h = float(int(sensor_data[6:10], 16))/100
                meter_ppm = int(sensor_data[10:14], 16)
                print("Type:" + meter_type + "\tTemp:"+ str(meter_temp) + "\tHume:" + str(meter_h) + "%" + "\tPPM:" + str(meter_ppm) + "Degree over:" + options.degree + " Will turn on Relay")
                if meter_temp > options.degree:
                    LED_Status = "01"
                else:
                    LED_Status = "00"
                subprocess.Popen(["./pub_dl_local.py", "-i", options.host, "-m", "05000006", "-g", str(gwid_data), "-c", "c", "-d", LED_Status])
            print('     Payload: ' + sensor_data + ' \x1b[6;30;42m' + 'HEX2ASCII:' + '\x1b[0m' + sensor_data.decode("hex"))
        except UnicodeDecodeError:
            print('     Payload: ' + sensor_data)
    if options.long_detail:
        print(json_data)


client = mqtt.Client(protocol=mqtt.MQTTv31)
try:
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(options.username, options.password)
# 這裏第三個參數可以調整，每個多少時間檢查MQTT 連線狀態，通常60秒已經算短的了，
# 爲了實驗，可以用60秒。2-5分鐘都算合理，google 的 GCM 都28分鐘檢查一次了，
# 在實際量產部署時，要重新考慮這個值，頻寬及Server Load 不是免費啊。

    try:
        client.connect(options.host, options.port, 60)
    except:
        print ('Can not connect to Broker')
        print ('Specify a IP address with option -i.')
        sys.exit()
    client.loop_forever()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("W: interrupt received, stopping..")
