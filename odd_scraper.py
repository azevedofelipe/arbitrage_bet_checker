# Script to scrape through oddspedia.com looking for good arbitrage betting odds (> 1% profit) and notifying of the bets found

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os

# Initialize day selection values
next_day = 2
count_day = 0
profit_bets = []

# List of all bookmakers scanned, and initalize blacklist as empty
bookmakers = ['1xBet', '20Bet', '22Bet', '31bet', '4rabet', 'Adjarabet', 'Amuletobet', 'BC.Game Sport', 'bet365', 'Bet7', 'Bet9', 'bet90', 'Betano', 'Betboo Sport',
            'Betcris', 'Betfair', 'Bethard', 'Betibet', 'BetKwiff', 'Betmotion Sport', 'Betobet', 'Betsafe', 'Betsson', 'Betsul', 'Bettilt', 'Betwarrior', 'Betway',
            'Betwinner', 'Blaze', 'BlueChip', 'Bodog', 'Bwin', 'Bzeebet', 'Cloudbet', 'ComeOn', 'Dafabet', 'Dafabet LATAM', 'Fezbet', 'Freshbet', 'Galera.Bet', 'GG.BET',
            'Goldenbet', 'Instabet', 'Ivibet', 'Jackbit', 'Kto', 'LeoVegas Sport', 'Loot.bet', 'LSbet', 'LVBET', 'Marathonbet', 'Megapari Sport', 'Midnite', 'Mostbet', 
            'Mr Green Sport', 'Mystake', 'NetBet', 'Nine Casino', 'Parimatch', 'Pin-up', 'Pinnacle', 'Powbet', 'Rivalo', 'Rivalry', 'Rolletto.com', 'Roobet', 'SnatchCasino',
            'Sportaza', 'Sportsbet.io', 'Stake.com', 'Suprabets', 'TonyBet', 'Vave', 'Weltbet', 'Zebet']
blacklist = []


# User configuration to choose sports to scrape for bets
urls = {"E-Sports":"https://oddspedia.com/br/esports/odds","Futebol":"https://oddspedia.com/br/futebol/odds","Basquete":"https://oddspedia.com/br/basquete/odds","Volei":"https://oddspedia.com/br/voleibol/odds",
        "Tenis":"https://oddspedia.com/br/tenis/odds","Ping Pong":"https://oddspedia.com/br/tenis-de-mesa/odds","Hoquei":"https://oddspedia.com/br/hoquei-no-gelo/odds","MMA":"https://oddspedia.com/br/artes-marciais-mistas/odds"}
user_urls = list(urls.values())
sports_selected = list(urls.keys())


# Prints all items in an array and its index + 1
def print_list(arr_urls):
    for (i,item) in enumerate(arr_urls,start=1):
        if(i < 10):
            print(f"[0{i}] - {item:^15}",end=' | ')
        else:
            print(f"[{i}] - {item:^15}",end=' | ')
        if i % 8 == 0:
            print()
    print()
    print("-"*200,end='\n')
        

# User blacklist configuration section
def user_bookmaker(blacklist,bookmakers):
    user_bookmaker_choices = -1
    while(user_bookmaker_choices != "C"):
        os.system('cls' if os.name == 'nt' else 'clear')
        if blacklist:
            print(f"Current blacklisted sites: {*blacklist,}")

        print_list(bookmakers)
        user_bookmaker_choices = input("Select bookmakers you would like to blacklist:\n[0] None\n[C] to Continue\n")

        match user_bookmaker_choices.upper():
            case "0":           # Selects all sports and continues
                user_bookmaker_choices = "C"
            case "C":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                user_bookmaker_choices = "C"
            case _:
                blacklist.append(bookmakers[int(user_bookmaker_choices)-1])
                bookmakers.pop(int(user_bookmaker_choices)-1)
    return blacklist,bookmakers


# Receives user input to select sports to scan
def user_sports(user_urls,sports_selected):
    user_sport_choices = -1
    while(user_sport_choices != "C"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_list(sports_selected)
        user_sport_choices = input("\nRemove the sports you would not like to scan for bets, (C) to continue: ")

        match user_sport_choices.upper():
            case "0":           # Selects all sports and continues
                pass
            case "C":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                pass
            case _:             # Removes user selected sport from list
                user_urls.pop(int(user_sport_choices)-1)
                sports_selected.pop(int(user_sport_choices)-1)

        # If no more sports available to select, break
        if not sports_selected:
            break
    return user_urls,sports_selected

def current_settings(settings_input):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Current settings:\nSports: {*sports_selected,}\nBlacklist: {*blacklist,}\n\n")
    settings_input = input("[E] - Edit Settings\n[C] - Run Script\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    return settings_input


os.system('cls' if os.name == 'nt' else 'clear')
user_settings_choice = -1
while user_settings_choice != "C":
    user_settings_choice = input("\nSettings:\n[1] - Blacklist Bookmakers\n[2] - Select Sports\n[3] - Settings\n[C] Continue\n")

    match user_settings_choice.upper():
        case "1":           # Selects all sports and continues
            blacklist,bookmakers = user_bookmaker(blacklist=blacklist,bookmakers=bookmakers)
        case "2":           # Sets next_day to 0 to skip main scanning loop if no sports selected
            user_urls,sports_selected = user_sports(user_urls=user_urls,sports_selected=sports_selected)
        case "3":
            user_settings_choice = current_settings(user_settings_choice)
        case "C":
            pass

if not user_urls:
    next_day = 0

# Scrape matches from every day until user decides to stop
while(next_day != 0):

    # Initialize selenium scraper
    service = Service()
    options = webdriver.ChromeOptions()
    d = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(d,10)

    # Outputs which sports will be scanned
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Blacklisted Bookmakers: ")
    if not blacklist:
        print("No blacklisted bookmakers")
    else:
        print(*blacklist,sep=', ')

    print("Scanning for bets in the following sports:")
    print(*sports_selected,sep=', ')


    for i,url in enumerate(user_urls,0):
        print(f"\n{sports_selected[i]}: ")
        print("-"*200,end='\n')

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

                # Filter out blacklisted bookmakers from profitable bets
                if(any(x in site for x in blacklist) and rolling_sum >= 1 and rolling_sum != 0):
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
    user_next_day = input("\nAccess specific bet data by index: (I) \nContinue to next day: (Y) \nRescan current day: (R) \nExit: (E) \n")
    match user_next_day:
        case "Y":
            print(f"Scanning next days matches...")
            next_day = 1
            count_day += 1
        case "E":
            print(f"Exiting...")
            next_day = 0
            break
        case "R":
            print("Rescanning...")
            next_day = next_day
            count_day = count_day
        case "I":
            bet_index = int(input("Enter match number: "))
            print(*profit_bets[bet_index-1])
            #Add way to go deeper into details
            user_next_day = input("\nAccess specific bet data by index: (I) \nContinue to next day: (Y) \nRescan current day: (R) \nExit: (E) \n")
        case _:
            print("Please enter a valid input!")
            user_next_day = input("\nAccess specific bet data by index: (I) \nContinue to next day: (Y) \nRescan current day: (R) \nExit: (E) \n")


# ADD THE CALCULATOR FROM THE WEBSITE
# ADD ALL GOOD BETS TO A LIST, ALLOW USER TO GET DETAILS (SUCH AS CALCULATOR) ABOUT A SPECIFIC MATCH USING ITS INDEX


# LOOK FOR OVER UNDER OPPORTUNITIES