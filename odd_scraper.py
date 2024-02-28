# Script to scrape through oddspedia.com looking for good arbitrage betting odds (> 1% profit) and notifying of the bets found

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Initialize selenium scraper
service = Service()
options = webdriver.ChromeOptions()
d = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(d,10)



urls = ["https://oddspedia.com/br/esports/odds","https://oddspedia.com/br/futebol/odds","https://oddspedia.com/br/basquete/odds","https://oddspedia.com/br/voleibol/odds",
        "https://oddspedia.com/br/tenis/odds","https://oddspedia.com/br/tenis-de-mesa/odds","https://oddspedia.com/br/hoquei-no-gelo/odds","https://oddspedia.com/br/artes-marciais-mistas/odds"]

# Future implementation of list of blacklisted sites, currently using string
blacklist = ["Betwinner"]

next_day = 2
count_day = 0
profit_bets = []

# Scrape matches from every day until user decides to stop
while(next_day != 0):
    for url in urls:
        print("-"*180,end='\n')

        d.get(url)

        #Go to next day bets
        if(next_day != 2):
            for i in range(count_day):
                wait.until(EC.presence_of_element_located((By.CLASS_NAME,"nav-calendar-mobile__next")))
                OddsNav = d.find_element(By.CLASS_NAME,"nav-calendar-mobile__next").click()
        
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.odd__logo > img")))
            matches = d.find_elements(By.CLASS_NAME,"match")
        except (NoSuchElementException,TimeoutException):
            print("No Events")
            continue

        count = 0
        blocked_count = 0
        #Loops through all matches scraped
        for x, match in enumerate(matches,1):

            # Filters the odds and link for each match
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.odd__logo > img")))
            odds_raw = match.find_elements(By.CLASS_NAME,'match-odds')
            odds = odds_raw[0].text.splitlines()

            # Gets the sites the best odds are on, can be used to filter out specific sites
            site = []
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.odd__logo > img")))
            logos = match.find_elements(By.CSS_SELECTOR,'span.odd__logo > img')

            for logo in logos:
                site.append(logo.get_attribute("alt"))
                
            # Gets match link and game status
            link = match.find_element(By.TAG_NAME,"a").get_attribute("href")
            status = match.find_element(By.CLASS_NAME,"match-state")

            # Ignores matches without odds, finished games or ongoing games
            if("ODDS INDISPON" in match.text or "Jogando" in status.text or "FT" in status.text or ":" not in status.text):
                continue
            else:
                rolling_sum = 0
                # Calculates arbitrage odds for each match independent of how many values per match (Win,Draw,Loss or Win,Loss)
                for value in odds:
                    rolling_sum += (1/float(value))

                # Calculates as a percentage of profit for user    
                rolling_sum = (1 - rolling_sum) * 100

                if("Betwinner" in site and rolling_sum >= 1 and rolling_sum != 0):
                    blocked_count += 1
                    rolling_sum = 0

                #Filters only profitable bets
                if(rolling_sum >= 1 and rolling_sum != 0):
                    count += 1
                    curr_bet = [status.text,*odds,rolling_sum,link,*site]
                    profit_bets.append(curr_bet)
                    print(f"[{len(profit_bets)}] {status.text} | Match: {*odds,} - Odds: {rolling_sum:.2f}%  -  {link} - Sites: {*site,}")
        
        # Display number of good bets and number of blacklisted bets
        if(count == 0):
            print(f"No good odds | Blocked: {blocked_count}")
        else:
            print(f"{count} Good Odds | Blocked: {blocked_count}")

    # Get user input to end or go to next day
    print("-"*180,end='\n')
    user_next_day = input("Access specific bet data by index: (I) \nContinue to next day: (Y) (N) \nRescan current day: (R) \n")
    match user_next_day:
        case "Y":
            print(f"Scanning next days matches...")
            next_day = 1
            count_day += 1
        case "N":
            print(f"Exiting...")
            next_day = 0
        case "R":
            print("Rescanning...")
            next_day = next_day
            count_day = count_day
        case "I":
            bet_index = int(input("Enter bet number: "))
            print(*profit_bets[bet_index-1])
            user_next_day = input("Access specific bet data by index: (I) \nContinue to next day: (Y) (N)\n")


# ADD SUPPORT TO CHANGE REGIONS, DICT WITH ALL REGIONS AND SWITCH
# ADD THE CALCULATOR FROM THE WEBSITE
# ADD ALL GOOD BETS TO A LIST, ALLOW USER TO GET DETAILS (SUCH AS CALCULATOR) ABOUT A SPECIFIC MATCH USING ITS INDEX
# LOOK FOR OVER UNDER OPPORTUNITIES