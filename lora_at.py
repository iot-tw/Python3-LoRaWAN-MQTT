import serial
import serial.tools.list_ports
com_port_list = []
for port in list(serial.tools.list_ports.comports()):
    com_port_list.append(port.device)
    print(port)
com_device_name = input(com_port_list)
ser = serial.Serial(com_device_name,9600, timeout=1)
ser.write(b"at+cadr?\r")
real_text = ser.readlines()

print([x.decode() for x in real_text])
