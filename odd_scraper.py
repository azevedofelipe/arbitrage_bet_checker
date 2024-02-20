# Script to scrape through oddspedia.com looking for good arbitrage betting odds (< 1.00) and notifying of the bets found
import requests
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://oddspedia.com/br/futebol/odds"
headers = {'Accept-Encoding': 'identity','User-Agent':'Chrome'}

service = Service()
options = webdriver.ChromeOptions()
d = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(d,5)

d.get(url)
wait.until(EC.presence_of_element_located((By.CLASS_NAME,"match-odds")))
matches = d.find_elements(By.CLASS_NAME,"match-odds")

for match in matches:
    odds = d.find_elements(By.CLASS_NAME,"bookmaker-link cursor-pointer odd")
    for odd in odds:
        value = d.find_element(By.CLASS_NAME,'odd__value')
        print(value.text)