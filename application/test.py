import requests, sys, os, zipfile, time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime, timedelta
import serial
from serial.tools.list_ports import comports
import time


def find_arduino_port():

    '''
    Find the Arduino serial communication (USB) port
    '''
    ports = comports()
    for port, desc, hwid in ports:
        if "Arduino" in desc or "CH340" in desc: 
            return port
    return None

def parse_sensor_data(data):
    
    '''
    Parse data received from the Arduino (UNO)
    '''
    data_list = data.split(',')
    temp = float(data_list[0].split(':')[1])
    humidity = float(data_list[1].split(':')[1])
    brightness = int(data_list[2].split(':')[1])
    return temp, humidity, brightness

arduino_port = find_arduino_port()
if arduino_port:
    print(f"[ACK] Arduino (UNO) found on port: {arduino_port}")
    ser = serial.Serial(arduino_port, 9600)  # Open serial connection
    try:
        while True:
            if ser.in_waiting > 0:
                raw_data = ser.readline().decode().strip()
                print(f"[ACK] RAW Arduino (UNO) data received: {raw_data}")
                temperature, humidity, bright = parse_sensor_data(raw_data)
                processed_data = f"temperature: {temperature}, humidity: {humidity}, brightness: {bright}"
                print(f"[ACK] Processed Arduino (UNO) data: {processed_data}")
            time.sleep(1)
    except KeyboardInterrupt:
        ser.close()
else:
    print(f"[ERR] Arduino (UNO) NOT found")
    sys.exit(7)