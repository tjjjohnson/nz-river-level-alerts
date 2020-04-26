#!/usr/bin/env python3

#code is based on ...
#https://medium.com/@manivannan_data/python-selenium-on-aws-lambda-b4b9de44b8e1
#https://github.com/ManivannanMurugavel/selenium-python-aws-lambda


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
from bs4 import BeautifulSoup
import bios
import boto3
import shutil

def get_river_levels_df():
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
    df = pd.read_html(str(rainfall_table))[0]
    df.columns = ['Location', 'DateTime', 'Level', 'Flow', 'RiseOrFall', 'AboveOrBelowFloodWarning']

    driver.close()
    driver.quit()

    return df

def alert_messsage(alert):
    return f"{alert['Location']} is {alert['Direction']} {alert['Level']}m \n"

def lambda_handler(event, context):
    # copy river level alerts yaml from s3 using RIVER_LEVEL_ALERTS_
    rules_tmp_file = '/tmp/river-level-alerts-rules.yaml'

    if 'RIVER_LEVEL_ALERTS_RULES_YAML' in os.environ:
        print(f"Using rules from environment variable RIVER_LEVEL_ALERTS_RULES_YAML={os.environ['RIVER_LEVEL_ALERTS_RULES_YAML']}")
        if os.environ['RIVER_LEVEL_ALERTS_RULES_YAML'].startswith('s3://'):
            s3_path = os.environ['RIVER_LEVEL_ALERTS_RULES_YAML'][5:]
            s3_components = s3_path.split('/')
            bucket = s3_components[0]
            s3_key = '/'.join(s3_components[1:])
            s3 = boto3.resource('s3')
            s3.Bucket(bucket).download_file(s3_key, rules_tmp_file)
        else:
            shutil.copyfile(os.environ['RIVER_LEVEL_ALERTS_RULES_YAML'], rules_tmp_file )
    else:
        print("Using default rules from example_alert_rules.yaml, override with RIVER_LEVEL_ALERTS_RULES_YAML which can read from s3 using s3://some_bucket/your_rules.yaml")
        shutil.copyfile('example_alert_rules.yaml', rules_tmp_file)

    alerts = bios.read(rules_tmp_file)
    print(alerts)

    df = get_river_levels_df()
    print(df)

    messages=""

    for alert in alerts:
        level_for_location = df[df['Location'] == alert['Location']]['Level'].values[0]
        if alert['Direction'] == 'above':
            if level_for_location > alert['Level']:
                messages += alert_messsage(alert)
        elif alert['Direction'] == 'below':
            if level_for_location < alert['Level']:
                messages += alert_messsage(alert)
        else:
            print(f"alert for {alert['Location']} has invalid direction {alert['Direction']}")
            os.sys.exit(1)

    print(messages)

    if messages != "":
        ses = boto3.client('ses')
        response = ses.send_email(
            Source = os.environ['RIVER_LEVEL_ALERTS_EMAIL_ADDRESS'],
            Destination={
                'ToAddresses': [
                    os.environ['RIVER_LEVEL_ALERTS_EMAIL_ADDRESS'],
                ]
            },
            Message={
                'Subject': {
                    'Data': 'River level alert'
                },
                'Body': {
                    'Text': {
                        'Data': messages
                    }
                }
            }
        )

    response = {
        "statusCode": 200,
        "body": messages
    }

    return response

if __name__ == "__main__":
   lambda_handler(None, None)
   

   
