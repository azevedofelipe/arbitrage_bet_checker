from logger import logger
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json
import re
import pandas as pd


def create_driver():
    return Driver(uc=True,headless=True)


def call_api(driver, url: str):
    if api := re.search(r'api/v1/([^?]*)',url):
        logger.log(f'Starting API call to {api.group(1)}')

    driver.get(url)
    # wait = WebDriverWait(driver,5)
    
    try:
        # wait.until(EC.presence_of_element_located((By.TAG_NAME,'pre')))
        pre_element = driver.find_element(By.TAG_NAME, 'pre').text
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