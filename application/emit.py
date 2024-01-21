import requests, sys, os, zipfile, time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime, timedelta
import serial
from serial.tools.list_ports import comports
import time

# Constants for terminal color codes.
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
ORANGE = '\033[38;2;255;165;0m'
BROWN = '\033[38;2;165;42;42m'
NC = '\033[0m'

# -------------------
# AUXILIARY FUNCTIONS
# -------------------

def download_zip(url):

    '''
    Download the zip file containing IoT Core certificates using a presigned URL
    '''

    response = requests.get(url)
    if response.status_code == 200:
        with open('certs.zip', 'wb') as file:
            file.write(response.content)
        print(f"{GREEN}[1/4] Certificates SUCESSFULLY downloaded{NC}")
        return True
    else:
        print(f"{RED}[ERR] Certificate download failed{NC}")
        return False

def unpack_zip(zip):

    '''
    Unpack the IoT Core certificates
    '''

    with zipfile.ZipFile(zip, 'r') as zip_ref:
        zip_ref.extractall('certs')
    print(f"{GREEN}[2/4] Certificates SUCESSFULLY extracted{NC}")

def MQTT_callback(client, topic, message):
    
    '''
    Process and store MQTT messages recursively
    '''
    message = message.payload.decode("utf-8")
    global CLIENT_STATUS
    
    print(f"(MQTT) Message {GREEN}received{NC}:")
    print(f"\t - topic: {BROWN}{MQTT_TOPIC}{NC}")
    print(f"\t - content: {BLUE}{message}{NC}")

def MQTT_publish(client, message):

    '''
    Publish a message using the configured MQTT client
    '''
    client.publish(MQTT_TOPIC, message, 1)
    print(f"(MQTT) Message {ORANGE}published{NC}:")
    print(f"\t - topic: {BROWN}{MQTT_TOPIC}{NC}")
    print(f"\t - content: {BLUE}{message}{NC}\n")

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

if __name__ == '__main__':

    # Extracting environment variables
    url = sys.argv[1] 
    USER_ID = sys.argv[2]

    CA = "./certs/awsCA.pem"
    CERTIFICATE = "./certs/user_certificate.crt"
    PKEY = "./certs/user_pkey.key"
    MQTT_ID = f"client-node-{USER_ID}"  
    MQTT_TOPIC = f"user-{USER_ID}-MQTT"
    ENDPOINT = "a2brwenekog21c-ats.iot.eu-central-1.amazonaws.com"

    if os.path.exists(CERTIFICATE) and os.path.exists(PKEY):
        print(f"{GREEN}[1/4][2/4] Certificates found. Skipping download{NC}")
    elif not url or not download_zip(url):
        print(f"{RED}[ERR] Invalid URL. Terminating program{NC}")
        sys.exit(5)
    else:
        unpack_zip('certs.zip')

    # Defining additional variables
    CA = "./certs/awsCA.pem"
    CERTIFICATE = "./certs/user_certificate.crt"
    PKEY = "./certs/user_pkey.key"
    MQTT_ID = f"client-node-{USER_ID}"  
    MQTT_TOPIC = f"user-{USER_ID}-MQTT"
    ENDPOINT = "a2brwenekog21c-ats.iot.eu-central-1.amazonaws.com"

    # MQTT client setup
    mqtt_client = AWSIoTMQTTClient(f"client-node-{USER_ID}")
    mqtt_client.configureEndpoint(ENDPOINT, 8883)
    mqtt_client.configureCredentials(CA, PKEY, CERTIFICATE)

    # Connect and subscribe to AWS IoT Core topic
    mqtt_client.connect()
    if not mqtt_client.subscribe(MQTT_TOPIC, 0, MQTT_callback):
        print(f"{RED}[ERR] Subscription FAILED{NC}")
        sys.exit(6)
    else: 
        print(f"{GREEN}[3/4] Subscription to topic {BROWN}{MQTT_TOPIC} {GREEN}SUCCESSFUL{NC}")

    print(f"{GREEN}[4/4] All prerequisites PASSED. Initializing MQTT data flux (CLIENT node) for user {BLUE}{USER_ID}{NC}\n")

    # Status message publish
    MQTT_publish(mqtt_client, f"CLIENT node {USER_ID} connected")

    # Emit Arduino data
    arduino_port = find_arduino_port()
    if arduino_port:
        print(f"{BLUE}[ACK]{NC} Arduino (UNO) found on port: {arduino_port}")
        ser = serial.Serial(arduino_port, 9600)  # Open serial connection
        try:
            while True:
                if ser.in_waiting > 0:
                    raw_data = ser.readline().decode().strip()
                    print(f"{BLUE}[ACK]{NC} RAW Arduino (UNO) data received: /n{raw_data}/n")
                    temperature, humidity, bright = parse_sensor_data(raw_data)
                    processed_data = f"temperature: {temperature}, humidity: {humidity}, brightness: {bright}"
                    MQTT_publish(mqtt_client, processed_data)
                time.sleep(1)
        except KeyboardInterrupt:
            ser.close()
    else:
        print(f"{RED}[ERR] Arduino (UNO) NOT found{NC}")
        sys.exit(7)