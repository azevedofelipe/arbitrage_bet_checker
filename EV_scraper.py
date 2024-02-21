# Script to scrape through oddspedia.com looking for good arbitrage betting odds (< 1.00) and notifying of the bets found
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://oddspedia.com/br/esports/odds"

service = Service()
options = webdriver.ChromeOptions()
d = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(d,5)

d.get(url)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,"nav-calendar-mobile__next")))
OddsNav = d.find_element(By.CLASS_NAME,"nav-calendar-mobile__next").click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME,"match-odds")))
matches = d.find_elements(By.CLASS_NAME,"match-odds")

#Default bet amount used to calculate EV
BASE_BET = 10

#Loops through all matches scraped
for x, match in enumerate(matches,1):
    # Ignores matches without odds
    if("ODDS INDISPON" in match.text):
        continue

    match_values = match.text.splitlines()
    print()
    print(f"Match {x}: ", end=' - ')

    # Calculates EV odds for each match independent of how many values per match (Win,Loss)
    for value in match_values:
        curr_fair_odds = 0
        sum_odds = 0
        final_odds = []

        for value_2 in match_values:
            sum_odds += float(value_2)

        curr_fair_odds = 1 / (sum_odds / len(match_values))
        rest_odds = 1 - curr_fair_odds
        curr_bet_profit = (float(value) * BASE_BET) - BASE_BET
        rest_profit = -(BASE_BET)

        curr_result = ((curr_bet_profit * curr_fair_odds) + (rest_profit * rest_odds))
        if(curr_result > 0):
            print(f"[EV: {value}] ${curr_bet_profit:.2f} x {curr_fair_odds:.4f} + ${rest_profit} x {rest_odds:.4f} = {curr_result:.4f} | ",end='')


#TO-DO: CHANGE TO BETWAY LINK OR SOME BETTING SITE