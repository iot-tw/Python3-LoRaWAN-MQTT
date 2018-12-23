#! /usr/bin/python
# -*- coding: utf8 -*-
__author__ = "Marty Chao"
__version__ = "1.0.3"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.1, init version
# Change log 1.0.2 default connect to lazyengineers
# Change Log 1.0.3 format for PEP8
import paho.mqtt.client as mqtt
import socket
import random
from optparse import OptionParser
import time
now_time = time.strftime("%Hc%Mc%S")
usage = "usage: %prog [options] [data]\n \
    e.g.: '%prog --data \"12345678901\" will downlink to module 04000476 \
    by Localhost Broker,Class A confirmed"
parser = OptionParser(usage)
parser.add_option("-d", "--data", action="store", dest="data",
                  default=now_time,
                  help="for sending HEX data")
parser.add_option("-c", "--class", action="store", dest="classtype",
                  default="A",
                  help="[A|a|C|c] for Class Mode.  Default is Class A\n \
                Lowercase is unconfimed message,Uppercase is confirmed\n")
parser.add_option("-i", "--ip", action="store", dest="host",
                  default="mqtt.lazyengineers.com",
                  help="IP for which MQTT Broker. \
                  Default is  mqtt.lazyengineers.com")
parser.add_option("-u", "--user", action="store",
                  dest="username", default="lazyengineers",
                  help="sub from MQTT broker's username ")
parser.add_option("-P", "--pw", action="store",
                  dest="password", default="lazyengineers",
                  help="sub from MQTT broker's password ")
parser.add_option("-p", action="store",
                  dest="port", default=1883,
                  help="sub from MQTT broker's Port ")
parser.add_option("-g", "--gid", action="store", dest="GID",
                  default="00001c497b431fcd",
                  help="GID for DL GW. Default is 00001c497b431fcd")
parser.add_option("-m", "--mac", action="store", dest="MAC",
                  default="04000476",
                  help="setting DL target Moudle MAC")
(options, args) = parser.parse_args()
if options.data:
    data = options.data
mid = "".join(map(lambda t: format(t, "02X"), [random.randrange(256)
                                               for x in range(16)]))
GID = options.GID
MAC = options.MAC
topic = "GIOT-GW/DL/" + GID
txpara = "6"
if options.classtype == "a":
    txpara = '"2"'
elif options.classtype == "A":
    txpara = '"6"'
elif options.classtype == "c":
    txpara = '"22"'
elif options.classtype == "C":
    txpara = '"26"'
elif options.classtype == "B":
    print("Not Support yet.")
msg = '[{"macAddr":"00000000' + MAC + '",' \
    + '"data":"' + data + '",' \
    + '"id":"' + mid + '",' \
    + '"extra":{"port":2, "txpara":' + txpara + '}}]'
print("Broker:" + options.host + " Topic:" +
      topic + " Class Mode:" + options.classtype)
print(msg)
client = mqtt.Client(protocol=mqtt.MQTTv31)
try:
    client.username_pw_set(options.username, options.password)
    client.connect(options.host, options.port, 60)
except socket.error as e:
    print(f"Can't Connect to {options.host}")
    print("May use -i to specify broker server?")

client.publish(topic, msg)
client.disconnect()
