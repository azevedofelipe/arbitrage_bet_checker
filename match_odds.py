from utils.logger import logger
from utils.utils import create_driver, call_api, format_date, list_all_days, list_available_sports
import pandas as pd
from settings import Settings


DROP_COLS = ['odd_name','value','bid','link','slug','bookie','status','offerId']

class MatchOdds:
    def __init__(self, settings: Settings):
        self.driver = create_driver()
        self.list_days = list_all_days(settings.days_scan)
        self.floor_profit = settings.floor_profit
        self.status = settings.match_status
        self.df_list = []
        self.available_sports = list_available_sports(self.driver,self.list_days,settings)
        self.profitable = 0

        # Currently calling for each sport and then for each day, would need to make it so it calls the day and then sports for that day
        self.df = self.get_all_odds()
        self.driver.quit()

        if not self.df.empty:
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
        except Exception as e:
            logger.log(f'Error making matches single line: {e}','error')
            exit()
    

    def fetch_and_normalize_data(self, url: str) -> pd.DataFrame | None:
        if json := call_api(self.driver, url):
            match_data = json['data']
            df = pd.json_normalize([{**item, 'matchId':key} for key, items in match_data.items() if isinstance(items,list) for item in items])
            logger.log(f'Found {len(df)} matches')

            df = df[df['status'] == 3]

            if not df.empty: 
                logger.log('Got matches that havent started')
                return df

        return None


    def get_all_odds(self):
        try:
            df_list = []

            for days, sports in self.available_sports.items():
                start_day = days[0]
                end_day = days[1]
                for sport in sports:
                    url = f'https://oddspedia.com/api/v1/getMaxOddsWithPagination?geoCode=BR&bookmakerGeoCode=BR&bookmakerGeoState=&wettsteuer=0&startDate={start_day}T03%3A00%3A00Z&endDate={end_day}T02%3A59%3A59Z&sport={sport}&excludeSpecialStatus=0&popularLeaguesOnly=0&sortBy=default&status={self.status}&page=1&perPage=600&inplay=0&language=en'
                    logger.log(f'Calling API for {sport} on {start_day}')
                    self.sport = sport

                    clean_data = self.fetch_and_normalize_data(url)

                    if clean_data is None:
                        logger.log(f'No match results found for {sport} on date {start_day}')
                        continue

                    self.df = clean_data
                    self.single_line_matches()

                    self.df['profit'] = self.df['odds'].apply(self.get_profit_percent)
                    logger.log('Got match profits')

                    self.df = self.df[self.df['profit'] >= self.floor_profit]
                    logger.log(f'Filtered {len(self.df)} profitable matches')

                    self.df = self.get_match_info()
                    logger.log('Got match info for all profitable bets')
                    
                    df_list.append(self.df)

            if df_list:
                return pd.concat(df_list,ignore_index=True)
            
            return pd.DataFrame()

        except Exception as e:
            logger.log(f'Failed to get all match odds: {e}','error')
            return pd.DataFrame()


    def get_match_info(self):
        self.df = self.df.assign(home=None, away=None, time=None, league=None, url=None)

        unique_matches = self.df['matchId'].unique()
        
        for match in unique_matches:
            url = f"https://oddspedia.com/api/v1/getMatchInfo?geoCode=BR&wettsteuer=0&r=wv&matchId={match}&language=en"
            logger.log(f'Getting match info for {match}')

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
