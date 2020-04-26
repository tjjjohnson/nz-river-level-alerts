#!/bin/bash

# Get chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip -o chromedriver.zip -d bin/
rm chromedriver.zip

# Get Headless-chrome
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip -o headless-chromium.zip -d bin/
rm headless-chromium.zip

chmod +x bin/*

#sudo apt install python3-pip zip unzip 
sudo yum install -y python3-pip

mkdir --parents lib bin
rm -r lib/*

curl -SL https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/raw/master/lib/libORBit-2.so.0 > lib/libORBit-2.so.0
curl -SL https://github.com/ManivannanMurugavel/selenium-python-aws-lambda/raw/master/lib/libgconf-2.so.4 > lib/libgconf-2.so.4

pip3 install -r requirements.txt -t lib 
pip3 install boto3 -t lib # install here as it's not needed for lambda?

export PYTHONPATH=${PYTHONPATH}:${PWD}/lib

export PATH=${PATH}:${PWD}/bin

# trying to fix 127 error
sudo yum install -y mesa-libOSMesa-devel
sudo yum install -y libX11
sudo yum install -y fontconfig