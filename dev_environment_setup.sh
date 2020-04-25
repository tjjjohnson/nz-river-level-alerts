#!/bin/bash

sudo apt install python3-pip zip unzip 

# download Selenium 2.37
$ pip3.6 install -t seleniumLayer/selenium/python/lib/python3.6/site-packages requirements

# download chrome driver
cd seleniumLayer
mkdir chromedriver
cd chromedriver
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
unzip -o chromedriver.zip
rm chromedriver.zip

# download chrome binary
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
unzip -o headless-chromium.zip
rm headless-chromium.zip

sudo apt install npm
npm config set prefix /usr/local
sudo npm i -g serverless


export PATH=${PATH}:~/Selenium-UI-testing-with-AWS-Lambda-Layers/chromedrive