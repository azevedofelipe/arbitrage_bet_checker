from datetime import date,timedelta
from match_odds import MatchOdds
from logger import logger


TODAY = str(date.today())
TMRW = str(date.today() + timedelta(days=1))
DROP_COLS = ['odd_name','value','bid','link','slug','bookie','status','offerId']


def main():
    football_profit = MatchOdds('football',TODAY,TMRW,0,'prematch')
    
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