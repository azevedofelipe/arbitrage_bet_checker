from seleniumbase import Driver
import json
from datetime import date,timedelta
from logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from typing import Literal


# TODAY = str(date.today())
TODAY = str(date.today() + timedelta(days=1))
TMRW = str(date.today() + timedelta(days=2))
DROP_COLS = ['odd_name','value','bid','link','slug','bookie','status','offerId']


# Ugly ass code, change later
class OddsAnalyzer:
    def __init__(self, sport: str, start_date: str, end_date: str, floor_profit: int, status: Literal['prematch','inplay','all']):
        self.sport = sport
        self.start_date = start_date
        self.end_date = end_date
        self.floor_profit = floor_profit
        self.status = status
        self.df = self.get_all_odds()
        self.profitable = len(self.df)

    @staticmethod
    def get_profit_percent(odds: list[dict]) -> float:
        profit = sum(1 / float(odd['value']) for odd in odds)
        profit_percent = round(((1/profit)-1) * 100,2)

        return profit_percent

    def single_line_matches(self):
        odds_df = self.df.groupby('matchId')[['odd_name','value','bookie']].apply(lambda x: x.to_dict('records')).reset_index(name='odds')
        self.df = self.df.drop_duplicates(subset='matchId')
        self.df = self.df.merge(odds_df, on='matchId',how='left')
        logger.log('Made all matches a single row')




    def get_all_odds(self):
        url = f'https://oddspedia.com/api/v1/getMaxOddsWithPagination?geoCode=BR&bookmakerGeoCode=&bookmakerGeoState=&wettsteuer=0&startDate={self.start_date}T03%3A00%3A00Z&endDate={self.end_date}T02%3A59%3A59Z&sport={self.sport}&ot=100&excludeSpecialStatus=0&popularLeaguesOnly=0&sortBy=default&status={self.status}&page=1&perPage=600&inplay=0&language=en'
        logger.log('Calling API')

        try:
            if raw_json := call_api(url):
                match_data = raw_json['data']
                self.df = pd.json_normalize([{**item, 'matchId':key} for key, items in match_data.items() if isinstance(items,list) for item in items])
                logger.log(f'Found {len(self.df)} matches for {self.sport}')

                self.df = self.df[self.df['status'] == 3]

                # Clean match data, find profit matches and get more info on those
                if not self.df.empty: 
                    logger.log('Got matches that havent started')
                    self.single_line_matches()

                    self.df['profit'] = self.df['odds'].apply(self.get_profit_percent)
                    logger.log('Got match profits')

                    self.df = self.df[self.df['profit'] >= self.floor_profit]
                    logger.log(f'Filtered {len(self.df)} profitable matches')

                    self.df = self.get_match_info()
                    logger.log('Got match info')

                    return self.df

            logger.log('Failed to get all match odds','error')
            return False

        except:
            logger.log('Failed to get all match odds','error')
            return False


    def get_match_info(self):

        self.df['home'] = None
        self.df['away'] = None
        self.df['time'] = None
        self.df['league'] = None
        self.df['url'] = None

        unique_matches = self.df['matchId'].unique()
        
        for match in unique_matches:
            url = f"https://oddspedia.com/api/v1/getMatchInfo?geoCode=&wettsteuer=0&r=wv&matchId={match}&language=en"

            match_data = call_api(url)

            if match_data:
                match_data = match_data['data']

                new_values = {
                    'home': match_data.get('ht'), 
                    'away': match_data.get('at'), 
                    'time': match_data.get('starttime'), 
                    'league': match_data.get('league_name'),
                    'url': 'https://oddspedia.com' + match_data.get('uri')
                }

                self.df.loc[self.df['matchId'] == match, ['home', 'away', 'time', 'league', 'url']] = list(new_values.values())
                
        return self.df


    def clean_table(self,col_names: list):
        self.df = self.df.drop(columns=col_names)


    def display_matches(self):
        
        print('Sure Bets')
        print('-'*130)
        for index, row in self.df.iterrows():
            print(row['time'] + ' | ' + row['home'] + ' vs ' + row['away'] + ' | ' + str(row['profit']) + '% | ' + row['url']) 
            print('-'*130)


def create_driver():
    global driver
    driver = Driver(uc=True,headless=False)


def call_api(url: str):
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
    


def main():
    create_driver()
    football_profit = OddsAnalyzer('football',TODAY,TMRW,0,'prematch')
    
    if football_profit.df is not False:
        logger.log('Found profitable matches')
        football_profit.clean_table(DROP_COLS) 
        football_profit.display_matches()
        print(football_profit.profitable)

    #TODO Allow user to select start and end dates
    #TODO See if its possible to do date range greater than 1 day
    #TODO use regex on call_api url log text
    #TODO look into a user interface


if __name__ == '__main__':
    main()