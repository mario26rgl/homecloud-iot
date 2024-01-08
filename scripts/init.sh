#!/bin/bash
# stop script on error
set -e

# Path to your project directory
PROJECT_DIR="./application"

# Updating the application
if [ -d "$PROJECT_DIR" ]; then
    echo "Updating the client application..."
    cd "$PROJECT_DIR"
    git pull origin main  
else
    echo "Installation not found. Donwloading application files..."
    mkdir "$PROJECT_DIR"
    git clone https://github.com/mario26rgl/homecloud-iot ./application
fi

# Check to see if root CA file exists, download if not
if [ ! -f ./certs/root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > ./root-CA.crt
fi

# Create a Python virtual environment
printf "\nCreating Python virtual environment...\n"
python3 -m venv venv

# Activate the virtual environment
printf "\nActivating Python virtual environment...\n"
source venv/bin/activate

# Install Flask inside the virtual environment
printf "\nInstalling required packages...\n"
python3 -m pip install awsiotsdk

# Run pub/sub sample app using certificates downloaded in the package
printf "\nRunning MQTT application...\n"
# python3 MQTT.py --topic control-node-test --ca_file ./certs/root-CA.crt --cert ./certs/certificate.pem.crt --key ./certs/private-key.pem.key --endpoint a2brwenekog21c-ats.iot.eu-central-1.amazonaws.com