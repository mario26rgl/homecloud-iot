#!/bin/bash
# stop script on error
set -e

# Updating the application
printf "\nUpdating the client application...\n"
git pull origin main --force  

# Check to see if root CA file exists, download if not
if [ ! -f ./certs/root-CA.crt ]; then
  printf "\nDownloading AWS IoT Root CA certificate from AWS...\n"
  mkdir certs
  curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > ./certs/awsCA.pem
fi

# Create a Python virtual environment
printf "\nCreating Python virtual environment...\n"
python3 -m venv venv

# Activate the virtual environment
printf "\nActivating Python virtual environment...\n"
source venv/bin/activate

# Install Flask inside the virtual environment
printf "\nInstalling required package(s)...\n"
python3 -m pip install AWSIoTPythonSDK
python3 -m pip install requests
python3 -m pip install pyserial

# Run pub/sub sample app using certificates downloaded in the package
printf "\nRunning MQTT application...\n"
python3 emit.py $1 $2