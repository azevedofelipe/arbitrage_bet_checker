from datetime import date,timedelta
from match_odds import MatchOdds
from logger import logger
import pandas as pd
import time


START = date.today()
END = date.today() + timedelta(days=1)


def main():
    start = time.time()
    football_profit = MatchOdds('football',START,END,1,'prematch')
    
    if  isinstance(football_profit.df, pd.DataFrame):
        logger.log('Found profitable matches')
        football_profit.display_matches()
    
    print(f'Took {time.time() - start} seconds')

    #TODO Look into wait on call_api why it takes so long
    #TODO Allow user to select start and end dates
    #TODO look into how to run multiple drivers at once
    #TODO remake requirements.txt


if __name__ == '__main__':
    main()