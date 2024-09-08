from utils.logger import logger
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json
import re
import pandas as pd
from datetime import date,timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver(headless: bool = True):
    return Driver(uc=True,headless=headless)


def call_api(driver, url: str, attempts: int = 2):
    if api := re.search(r'api/v1/([^?]*)',url):
        logger.log(f'Starting API call to {api.group(1)}')

    wait = WebDriverWait(driver,3)
    
    for _ in range(1,attempts+1):
        try:
            logger.log(f'Calling API ({_}/{attempts})')
            driver.get(url)

            wait.until(EC.presence_of_element_located((By.TAG_NAME,'pre')))
            try:
                pre_element = driver.find_element(By.TAG_NAME, 'pre').text
                logger.log("Found JSON")
                json_data = json.loads(pre_element)
                logger.log('Returned JSON')
                return json_data

            except NoSuchElementException:
                logger.log("<pre> element not found")

        except json.JSONDecodeError as e:
            logger.log(f"Erro ao analisar JSON: {e}",'error')
        
        except Exception as e:
            logger.log(f'General Error {e}')


    return None

def format_date(date_str: str) -> str:
    dt = pd.to_datetime([date_str])
    formatted_date = dt.strftime('%d/%m %I %p')
    return formatted_date[0]


def get_start_end_days(days_count: int) -> tuple:
    current_date = date.today()
    end_date = current_date + timedelta(days=days_count)
    
    return (str(current_date), str(end_date))


def get_region_bookmakers(region: str, driver = None) -> dict:
    bookmakers = {}

    if not driver:
        driver = create_driver()

    url = f'https://oddspedia.com/api/v1/getBookmakers?geoCode={region}&geoState=&language=en'
    json = call_api(driver,url)

    if json:
        bookmakers = {item['name']: True for item in json['data']}
        logger.log(f'Got Bookmakers for {region}')

    if not driver:
        driver.quit()
    
    logger.log(f'{bookmakers}')
    return bookmakers
