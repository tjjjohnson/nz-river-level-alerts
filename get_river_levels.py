#!/usr/bin/env python3

# https://medium.com/hackernoon/running-selenium-and-headless-chrome-on-aws-lambda-layers-python-3-6-bd810503c6c3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def get_river_levels(event, context):
    options = Options()
    options.binary_location = os.path.join(os.getcwd(), 'bin', 'headless-chromium')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280x1696')
    options.add_argument('--user-data-dir=/tmp/user-data')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--enable-logging')
    options.add_argument('--log-level=0')
    options.add_argument('--v=99')
    options.add_argument('--single-process')
    options.add_argument('--data-path=/tmp/data-path')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--homedir=/tmp')
    options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    driver = webdriver.Chrome(os.path.join(os.getcwd(), 'bin', 'chromedriver'),chrome_options=options)

    driver.get('https://www.waikatoregion.govt.nz/services/regional-services/river-levels-and-rainfall/river-levels-and-flow-latest-reading/')
    body = f"Headless Chrome Initialized, Page title: {driver.title}"

    print(body)

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": body
    }

    return response

if __name__ == "__main__":
   get_river_levels(None, None)