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


def call_api(driver, url: str):
    if api := re.search(r'api/v1/([^?]*)',url):
        logger.log(f'Starting API call to {api.group(1)}')

    driver.get(url)
    wait = WebDriverWait(driver,3)
    
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME,'pre')))
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


def list_available_sports(driver, dates: dict, region: str) -> dict | bool:
    days = dict()

    for start_date,end_date in dates.items():
        url = f'https://oddspedia.com/api/v1/getLeagues?topLeaguesOnly=0&includeLeaguesWithoutMatches=0&startDate={start_date}T03%3A00%3A00Z&endDate={end_date}T02%3A59%3A59Z&geoCode={region}&language=en'
        json = call_api(driver,url)
        
        if not json:
            return False

        available_sports = {item['sport_slug'] for item in json['data']}
        days[start_date] = available_sports

    return days