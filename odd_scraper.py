# Script to scrape through oddspedia.com looking for good arbitrage betting odds (< 1.00) and notifying of the bets found
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import *

url = "https://oddspedia.com/br/esports/odds"
#url = "https://oddspedia.com/br/futebol/odds"
#url = "https://oddspedia.com/br/basquete/odds"
#url = "https://oddspedia.com/br/voleibol/odds"
#url = "https://oddspedia.com/br/artes-marciais-mistas/odds"
#url = "https://oddspedia.com/br/voleibol/odds"

service = Service()
options = webdriver.ChromeOptions()
d = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(d,5)

d.get(url)

#Go to next day bets
wait.until(EC.presence_of_element_located((By.CLASS_NAME,"nav-calendar-mobile__next")))
OddsNav = d.find_element(By.CLASS_NAME,"nav-calendar-mobile__next").click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME,"match")))
matches = d.find_elements(By.CLASS_NAME,"match")

count = 0
#Loops through all matches scraped
for x, match in enumerate(matches,1):

    #Filters the odds and link for each match
    odds = match.find_elements(By.CLASS_NAME,'match-odds')
    odds = odds[0].text.splitlines()

    link = match.find_element(By.TAG_NAME,"a").get_attribute("href")

    # Ignores matches without odds
    if("ODDS INDISPON" in match.text):
        continue
    else:
        rolling_sum = 0

        # Calculates arbitrage odds for each match independent of how many values per match (Win,Draw,Loss or Win,Loss)
        for value in odds:
            rolling_sum += (1/float(value))

        #Filters only profitable bets
        if(rolling_sum < 1.00):   
            print(f"[{x}] Match: {*odds,} - Odds: {rolling_sum:.4f}  -  {link}")
            count += 1

if(count == 0):
    print("No good odds")

#TO-DO: GET LINK FOR EACH MATCH AND DISPLAY IT
#       LOOP SEVERAL URLS