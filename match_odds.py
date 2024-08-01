from logger import logger
from utils import create_driver, call_api, format_date
import pandas as pd
from typing import Literal


DROP_COLS = ['odd_name','value','bid','link','slug','bookie','status','offerId']

# Ugly ass code, change later
class MatchOdds:
    def __init__(self, sport: str, start_date: str, end_date: str, floor_profit: int, status: Literal['prematch','inplay','all']):
        self.driver = create_driver()

        self.sport = sport
        self.start_date = start_date
        self.end_date = end_date
        self.floor_profit = floor_profit
        self.status = status
        self.df = self.get_all_odds()
        self.profitable = 0
        self.driver.quit()

        if isinstance(self.df,pd.DataFrame):
            self.profitable = len(self.df)
            self.clean_table(DROP_COLS)

    
    @staticmethod
    def get_profit_percent(odds: list[dict]) -> float:
        profit = sum(1 / float(odd['value']) for odd in odds)
        profit_percent = round(((1/profit)-1) * 100,2)

        return profit_percent


    def single_line_matches(self):
        try:
            odds_df = self.df.groupby('matchId')[['odd_name','value','bookie']].apply(lambda x: x.to_dict('records')).reset_index(name='odds')
            self.df = self.df.drop_duplicates(subset='matchId')
            self.df = self.df.merge(odds_df, on='matchId',how='left')
            logger.log('Made all matches a single row')
        except:
            logger.log('Error making matches single line','error')
            exit()
    

    def fetch_and_normalize_data(self, url: str) -> pd.DataFrame | None:
        if json := call_api(self.driver, url):
            match_data = json['data']
            df = pd.json_normalize([{**item, 'matchId':key} for key, items in match_data.items() if isinstance(items,list) for item in items])
            logger.log(f'Found {len(df)} matches for {self.sport}')

            df = df[df['status'] == 3]

            if not df.empty: 
                logger.log('Got matches that havent started')
                return df

        return None


    def get_all_odds(self):
        url = f'https://oddspedia.com/api/v1/getMaxOddsWithPagination?geoCode=BR&bookmakerGeoCode=&bookmakerGeoState=&wettsteuer=0&startDate={self.start_date}T03%3A00%3A00Z&endDate={self.end_date}T02%3A59%3A59Z&sport={self.sport}&ot=100&excludeSpecialStatus=0&popularLeaguesOnly=0&sortBy=default&status={self.status}&page=1&perPage=600&inplay=0&language=en'
        logger.log('Calling API')

        try:
            clean_data = self.fetch_and_normalize_data(url)

            if clean_data is None:
                logger.log(f'No match results found for {self.sport}')
                return None

            self.df = clean_data
            self.single_line_matches()

            self.df['profit'] = self.df['odds'].apply(self.get_profit_percent)
            logger.log('Got match profits')

            self.df = self.df[self.df['profit'] >= self.floor_profit]
            logger.log(f'Filtered {len(self.df)} profitable matches')

            self.df = self.get_match_info()
            logger.log('Got match info')

            return self.df

        except:
            logger.log('Failed to get all match odds','error')
            return None


    def get_match_info(self):
        self.df = self.df.assign(home=None, away=None, time=None, league=None, url=None)

        unique_matches = self.df['matchId'].unique()
        
        for match in unique_matches:
            url = f"https://oddspedia.com/api/v1/getMatchInfo?geoCode=&wettsteuer=0&r=wv&matchId={match}&language=en"

            match_data = call_api(self.driver,url)

            if match_data:
                match_data = match_data['data']

                new_values = {
                    'home': match_data.get('ht'), 
                    'away': match_data.get('at'), 
                    'time': format_date(match_data.get('starttime')),
                    'league': match_data.get('league_name'),
                    'url': 'https://oddspedia.com' + match_data.get('uri')
                }

                self.df.loc[self.df['matchId'] == match, ['home', 'away', 'time', 'league', 'url']] = list(new_values.values())
                
        return self.df


    def clean_table(self,col_names: list):
        self.df = self.df.drop(columns=col_names)


    #TODO Make this better, temporary prints
    def display_matches(self):
        print('Sure Bets')
        print('-'*130)
        if isinstance(self.df,pd.DataFrame):
            for index, row in self.df.iterrows():
                print(row['time'] + ' | ' + row['home'] + ' vs ' + row['away'] + ' | ' + str(row['profit']) + '% | ' + row['url']) 
                print('-'*130)
