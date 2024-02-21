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

#Loops through all matches scraped
for x, match in enumerate(matches,1):
    # Ignores matches without odds
    if("ODDS INDISPON" in match.text):
        continue

    rolling_sum = 0
    match_values = match.text.splitlines()

    # Calculates arbitrage odds for each match independent of how many values per match (Win,Draw,Loss or Win,Loss)
    for value in match_values:
        rolling_sum += (1/float(value))
    #Filters only profitable bets < 2% profit
    if(rolling_sum < 0.98):   
        print(f"[{x}] Match: {*match_values,} - Odds: {rolling_sum}")


#TO-DO: GET LINK FOR EACH MATCH AND DISPLAY IT
#       LOOP SEVERAL URLS