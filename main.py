from datetime import date,timedelta
from match_odds import MatchOdds
from logger import logger
import pandas as pd


TODAY = str(date.today())
TMRW = str(date.today() + timedelta(days=1))


def main():
    football_profit = MatchOdds('football',TODAY,TMRW,0,'prematch')
    
    if  isinstance(football_profit.df, pd.DataFrame):
        logger.log('Found profitable matches')
        football_profit.display_matches()
        print(football_profit.profitable)

    #TODO Look into wait on call_api why it takes so long
    #TODO Allow user to select start and end dates
    #TODO See if its possible to do date range greater than 1 day
    #TODO look into a user interface
    #TODO look into how to run multiple drivers at once


if __name__ == '__main__':
    main()