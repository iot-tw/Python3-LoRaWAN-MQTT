#! /usr/bin/env python3
__author__ = "Marty Chao"
__version__ = "1.0.3"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.1 init version
# Change log 1.0.2 default broker is lazyengineers
# Change log 1.0.3 format for PEP8

import paho.mqtt.client as mqtt
import socket
import random
import datetime
from optparse import OptionParser
import time

now_time = time.strftime("%Hc%Mc%S")
usage = 'usage: %prog [options] [data]\n \
    options: -d for sending data\n \
             -i IP for which MQTT Broker. Default is lazyengineers\n \
             -m MAC for DL Node. Default is 04000476 \n \
             -g GID . Default is 1C497B499010 \n \
    e.g.: \'%prog --data "1234567890" will UPLink to Broker'
parser = OptionParser(usage)
parser.add_option(
    "-d", "--data", action="store", dest="data", default=now_time, help="sending data"
)
parser.add_option(
    "-i",
    "--ip",
    action="store",
    dest="host",
    default="localhost",
    help="setting Broker IP",
)
parser.add_option(
    "-P",
    "--pw",
    action="store",
    dest="password",
    default="admin",
    help="sub from MQTT broker's password ",
)
parser.add_option(
    "-u",
    "--user",
    action="store",
    dest="username",
    default="admin",
    help="sub from MQTT broker's username ",
)
parser.add_option(
    "-p", action="store", dest="port", default=1883, help="sub from MQTT broker's Port "
)
parser.add_option(
    "-g",
    "--gwid",
    action="store",
    dest="GID",
    default="1C497B499010",
    help="setting GID",
)
parser.add_option(
    "-m",
    "--mac",
    action="store",
    dest="MAC",
    default="05000001",
    help="setting DL target Moudle MAC",
)
(options, args) = parser.parse_args()
if options.data:
    data = options.data
mid = str(random.randint(1, 99))
# This is IDU GID
# GID = "1C497B499010"
# GID = "1C497B4321AA"
# This is ODU GID
# GID = "00001c497b431fcd"
GID = options.GID
MAC = options.MAC
topic = "GIOT-GW/UL/" + GID
msg = (
    '[{"channel":923125000, "sf":10, '
    + '"time":"'
    + datetime.datetime.now().isoformat()[:19]
    + '", '
    + '"gwip":"192.168.88.1", '
    + '"gwid":"0000f835dde7de2", "repeater":"00000000ffffffff", '
    + '"systype":'
    + str(int(MAC[:2], 16))
    + ", "
    + '"rssi":-118.0, "snr":0.5, "snr_max":3.8, "snr_min":-4.5, '
    + '"macAddr":"00000000'
    + MAC
    + '", '
    + '"data":"'
    + data
    + '",'
    + '"frameCnt":"'
    + mid
    + '",'
    + '"port":2}]'
)
print("Broker:" + options.host + " Topic:" + topic)
print(msg)
client = mqtt.Client(protocol=mqtt.MQTTv31)
try:
    client.username_pw_set(options.username, options.password)
    client.connect(options.host, options.port, 60)
except socket.error as e:
    print(f"Error: {e}")
    print("Can't Connect to " + options.host)
    print("May use -i to specify broker server?")

client.publish(topic, msg)
client.disconnect()
