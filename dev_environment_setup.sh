#!/bin/bash

# Get chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip > chromedriver.zip
unzip -o chromedriver.zip -d bin/

# Get Headless-chrome
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-29/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip -o headless-chromium.zip -d bin/

sudo apt install python3-pip zip unzip 

mkdir --parents lib bin

pip3 install -r requirements.txt -t lib

