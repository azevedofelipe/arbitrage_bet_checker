from seleniumbase import Driver
import json
from datetime import date,timedelta
from logger import Logger
from selenium.webdriver.common.by import By

logger = Logger()

today = date.today()
tomorrow = date.today() + timedelta(days=1)

url = f"https://oddspedia.com/api/v1/getMaxOddsWithPagination?geoCode=BR&bookmakerGeoCode=BR&bookmakerGeoState=&wettsteuer=0&startDate={today}T03%3A00%3A00Z&endDate={tomorrow}T02%3A59%3A59Z&excludeSpecialStatus=0&popularLeaguesOnly=1&sortBy=default&status=all&page=1&perPage=250&inplay=0&language=en"
    
def create_driver():
    global driver
    driver = Driver(uc=True,headless=True)


def call_api(url: str):
    logger.log('Starting API call')
    driver.get(url)

    pre_element = driver.find_element(By.TAG_NAME, 'pre').text
    try:
        json_data = json.loads(pre_element)
        clean_data = list(json_data['data'].values())
        logger.log('Returned JSON')
        return clean_data
    except json.JSONDecodeError as e:
        logger.log(f"Erro ao analisar JSON: {e}",'error')
        return None
    
def get_profits(match_odds: list) -> float:
    rolling_sum = 0

    for odd in match_odds:
        rolling_sum += (1/float(odd['value']))

    percentage = round(((1/rolling_sum)-1) * 100,2)
    return percentage 


def main():
    create_driver()
    match_data = call_api(url)

    if match_data:
        print(match_data[0])
        print(get_profits(match_data[0]))
    

if __name__ == '__main__':
    main()