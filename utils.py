from logger import logger
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime


def create_driver():
    return Driver(uc=True,headless=False)


def call_api(driver, url: str):
    logger.log(f'Starting API call to {url[29:65]}')
    driver.get(url)
    wait = WebDriverWait(driver,5)
    
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME,'pre')))
        pre_element = driver.find_element(By.TAG_NAME, 'pre').text
        logger.log("Found JSON")
        json_data = json.loads(pre_element)
        logger.log('Returned JSON')
        return json_data

    except json.JSONDecodeError as e:
        logger.log(f"Erro ao analisar JSON: {e}",'error')
        return None


def format_date(date_str: str) -> str:
    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
    formatted_date = dt.strftime('%d/%m %I%p')
    formatted_date = formatted_date.replace(" 0", " ")
    return formatted_date