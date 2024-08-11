from utils.logger import logger
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json
import re
import pandas as pd
from datetime import date,timedelta
from selenium.common.exceptions import NoSuchElementException


def create_driver():
    return Driver(uc=True,headless=True)


def call_api(driver, url: str):
    if api := re.search(r'api/v1/([^?]*)',url):
        logger.log(f'Starting API call to {api.group(1)}')

    driver.get(url)
    # wait = WebDriverWait(driver,5)
    
    try:
        # wait.until(EC.presence_of_element_located((By.TAG_NAME,'pre')))
        try:
            pre_element = driver.find_element(By.TAG_NAME, 'pre').text

        except NoSuchElementException:
            logger.log("<pre> element not found")
            return None

        logger.log("Found JSON")
        json_data = json.loads(pre_element)
        logger.log('Returned JSON')
        return json_data

    except json.JSONDecodeError as e:
        logger.log(f"Erro ao analisar JSON: {e}",'error')
        return None


def format_date(date_str: str) -> str:
    dt = pd.to_datetime([date_str])
    formatted_date = dt.strftime('%d/%m %I %p')
    return formatted_date[0]

# Grabs all days upto end_date + 1 to filter urls
def list_all_days(start_date: date, end_date: date) -> dict[str,str]:
    current_date = start_date
    date_dict = {}

    while current_date <= end_date: 
        date_dict[str(current_date)] = str(current_date + timedelta(days=1))
        current_date += timedelta(days=1)
    
    return date_dict
