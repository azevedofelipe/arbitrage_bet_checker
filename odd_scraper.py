# Script to scrape through oddspedia.com looking for good arbitrage betting odds (< 1.00) and notifying of the bets found
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://oddspedia.com/br/futebol/odds"

service = Service()
options = webdriver.ChromeOptions()
d = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(d,5)

d.get(url)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,"nav-calendar-mobile__next")))
OddsNav = d.find_element(By.CLASS_NAME,"nav-calendar-mobile__next").click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME,"match-odds")))
matches = d.find_elements(By.CLASS_NAME,"match-odds")

for match in matches:
    if("ODDS INDISPON" in match.text):
        continue

    rolling_sum = 0
    print("Match: ",end='')

    match_values = match.text.splitlines()
    for value in match_values:
        rolling_sum += (1/float(value))
        print(f"{value} ",end='')
    print(f"Odds: {rolling_sum}")
