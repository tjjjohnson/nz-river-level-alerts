#!/usr/bin/env python3

#https://medium.com/@manivannan_data/python-selenium-on-aws-lambda-b4b9de44b8e1

#https://github.com/ManivannanMurugavel/selenium-python-aws-lambda

# https://medium.com/hackernoon/running-selenium-and-headless-chrome-on-aws-lambda-layers-python-3-6-bd810503c6c3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd

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
    title = f"Headless Chrome Initialized, Page title: {driver.title}"

    page_data=driver.page_source

    #https://medium.com/@kagemusha_/scraping-on-a-schedule-with-aws-lambda-and-cloudwatch-caf65bc38848
    content = BeautifulSoup(page_data, 'html.parser')
    rainfall_table = content.select('#RainfallTable')[0]
    userrows = [t for t in allrows if t.findAll(text=re.compile('abc123123'))]
    df = pd.read_html(str(rainfall_table))
    df.columns = ['Location', 'DateTime', 'Level', 'Flow', 'RiseOrFall', 'AboveOrBelowFloodWarning']

    print(df)

    #print(rainfall_table_rows)

    driver.close()
    driver.quit()

    response = {
        "statusCode": 200,
        "body": title
    }

    return response

if __name__ == "__main__":
   get_river_levels(None, None)