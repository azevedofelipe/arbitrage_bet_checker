from seleniumbase import Driver
import json
from datetime import date,timedelta
from logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


TODAY = str(date.today())
TMRW = str(date.today() + timedelta(days=1))

    
def create_driver():
    global driver
    driver = Driver(uc=True,headless=False)


def call_api(url: str):
    logger.log(f'Starting API call to {url[:20]}')
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
    

def get_profits(value):
    profit = (1 / value.astype(float)).sum()

    profit_percent = round((1 - profit) * 100,2)
    return profit_percent


def get_all_odds(sport: str,start_date: str, end_date: str, floor_profit: int) -> pd.DataFrame | bool:
    """ Get all match odds of sport from start_date to end_date >= floor_profit

    Args:
        sport (str): Sport to get match odds for (e.g football)
        start_date (str): Start date for filter
        end_date (str): End date for filter
        floor_profit (int): Floor profit, returns any matches >= floor_profit

    Returns:
        dict: Returns matchId, odds and profit %
    """

    url = f'https://oddspedia.com/api/v1/getMaxOddsWithPagination?geoCode=BR&bookmakerGeoCode=&bookmakerGeoState=&wettsteuer=0&startDate={start_date}T03%3A00%3A00Z&endDate={end_date}T02%3A59%3A59Z&sport={sport}&ot=100&excludeSpecialStatus=0&popularLeaguesOnly=0&sortBy=default&status=all&page=1&perPage=250&inplay=0&language=en'

    if raw_json := call_api(url):
        logger.log('Got all odds json')
        match_data = raw_json['data']
        df = pd.json_normalize([{**item, 'matchId':key} for key, items in match_data.items() if isinstance(items,list) for item in items])

        filtered_df = df[df['status'] == 3]

        # status == 3 means the match hasnt started yet
        if not filtered_df.empty: 
            logger.log('Got matches that havent started')

            profits = filtered_df.groupby('matchId')['value'].apply(get_profits).reset_index(name='profit')
            profits = pd.merge(filtered_df, profits, on='matchId',how='left')
            logger.log('Got match profits')

            df_profit = profits[profits['profit'] >= floor_profit]
            logger.log('Filtered out unprofittable matches')
            print(df_profit.head(15))

            return df_profit

    logger.log('Failed to get all match odds','error')
    return False

def main():
    create_driver()
    get_all_odds('football',TODAY,TMRW,1)

if __name__ == '__main__':
    main()