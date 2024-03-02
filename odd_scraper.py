# Script to scrape through oddspedia.com looking for good arbitrage betting odds (> 1% profit) and notifying of the bets found

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import time
from arb_calculator import calculator, print_calc_results, calculate_remaining_bets

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
        "Tenis":"https://oddspedia.com/br/tenis/odds","Ping Pong":"https://oddspedia.com/br/tenis-de-mesa/odds","Hoquei":"https://oddspedia.com/br/hoquei-no-gelo/odds","MMA":"https://oddspedia.com/br/artes-marciais-mistas/odds",
        "Futsal": "https://oddspedia.com/br/futsal/odds"}

user_urls = list(urls.values())
user_deselected_urls = []
sports_selected = list(urls.keys())
sports_deselected = []


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
        clear_terminal()
        if blacklist:
            print(f"Current blacklisted sites: {*blacklist,}")

        print_list(bookmakers)
        user_bookmaker_choices = input("Select bookmakers you would like to blacklist:\n[0] None\n[C] to Continue\n")

        match user_bookmaker_choices.upper():
            case "0":           # Selects all sports and continues
                user_bookmaker_choices = "C"
            case "C":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                clear_terminal()
            case _:
                blacklist.append(bookmakers[int(user_bookmaker_choices)-1])
                bookmakers.pop(int(user_bookmaker_choices)-1)
    return blacklist,bookmakers


# Receives user input to select sports to scan
def user_sports():
    global sports_selected,user_urls,sports_deselected,user_deselected_urls
    user_sport_choices = -1

    while(user_sport_choices != "C"):
        clear_terminal()
        user_sport_choices = input("\n[A] - Add Sports\n[R] - Remove Sports\n[B] - Back\n").upper()

        match user_sport_choices.upper():
            case "B":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                clear_terminal()
                break
            case "R":             # Removes user selected sport from list
                if sports_selected:
                    remove_index = -1
                    while remove_index != "C" and sports_selected:
                        clear_terminal()
                        print_list(sports_selected)
                        remove_index = input("Enter the sport you would like to remove, [C] - Close: ").upper()
                        if remove_index.isnumeric():
                            if int(remove_index) -1 < len(sports_selected) and int(remove_index) > 0:         # If input in list index range remove from user_urls and add to deselected
                                user_deselected_urls.append(user_urls.pop(int(remove_index)-1))
                                sports_deselected.append(sports_selected.pop(int(remove_index)-1))
                    if not sports_selected:
                        clear_terminal()
                        print("All sports deselected\n")
                        time.sleep(1)
                        clear_terminal()
            case "A":
                if sports_deselected:           # If there are sports to add
                    add_index = -1
                    while add_index != "C" and sports_deselected:           # Loop while user hasnt exitted and list isnt empty
                        clear_terminal()
                        print_list(sports_deselected)
                        add_index = input("Enter the sport you would like to add, [C] - Close: ").upper()

                        if add_index.isnumeric():
                            if int(add_index) -1 < len(sports_deselected) and int(add_index) > 0:         # If input in list index range remove from user_urls and add to deselected
                                user_urls.append(user_deselected_urls.pop(int(add_index)-1))
                                sports_selected.append(sports_deselected.pop(int(add_index)-1))
                    if not sports_deselected:
                        clear_terminal()
                        print("All sports added\n")
                        time.sleep(1)
                        clear_terminal()
            case _:
                print("Enter a valid input.")

        # If no more sports available to select, break
        if not sports_selected:
            break
    return user_urls,sports_selected


# Displays match info based on user input
def match_info(profit_bets):    
    for x,bet in enumerate(profit_bets,1):
        print(f"[{x}] Odds: {*bet[1],} - Sure Profit: {bet[2]}% - Bookmakers: {*bet[4],} - Link: {bet[3]}")

    bet_index = input("[C] - Close\nEnter match number: ").upper()

    if bet_index == "C":
        clear_terminal()
        return
    else:
        chosen_match = profit_bets[int(bet_index)-1]

    clear_terminal()
    print("Selected Match:")
    print(f"[{x}] Odds: {*chosen_match[1],} - Sure Profit: {chosen_match[2]}% - Bookmakers: {*chosen_match[4],} - Link: {chosen_match[3]}")
    user_match_choice = input("\n[C] - Calculator\n[B] - Bet Amount Calculator\n[R] - Return\n")
    
    match user_match_choice.upper():
        case "C":
            print_calc_results(calculator(chosen_match[1],None))
        case "B":
            calculate_remaining_bets(chosen_match[1])
        case "R":
            pass

# Clears terminal output for better interface
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Get user input to end or go to next day
def end_interface():
    global next_day,count_day,blacklist,bookmakers,user_urls,sports_selected

    print("-"*180,end='\n')
    user_next_day = -1
    while user_next_day != "C" or user_next_day != 'E':
        user_next_day = input("\n[I] - Access specific bet data by index\n[C] - Continue to next day\n[R] - Rescan current day\n[1] - Blacklist Bookmakers\n[2] - Select Sports\n[E] - Exit\n").upper()

        match user_next_day:
            case "C":
                print(f"Scanning next days matches...")
                next_day = 1
                count_day += 1
                break
            case "E":
                print(f"Exiting...")
                next_day = 0
                break
            case "R":
                print("Rescanning...")
                next_day = next_day
                count_day = count_day
                break
            case "I":
                if profit_bets:
                    clear_terminal()
                    match_info(profit_bets=profit_bets)
                else:
                    print("No good odds found")
            case "1":           # Selects all sports and continues
                blacklist,bookmakers = user_bookmaker(blacklist=blacklist,bookmakers=bookmakers)
            case "2":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                user_sports()
            case _:
                print("Please enter a valid input!")

def start_interface():
    global next_day,sports_selected,blacklist,user_urls,bookmakers,sports_deselected,user_deselected_urls
    user_settings_choice = -1

    while user_settings_choice != "C":
        print(f"Current settings:\nSports Selected: {*sports_selected,}\nBlacklist: {*blacklist,}")
        user_settings_choice = input("\nSettings:\n\n[1] - Blacklist Bookmakers\n[2] - Select Sports\n[C] - Continue\n[E] - Exit\n").upper()

        match user_settings_choice.upper():
            case "1":           # Selects all sports and continues
                blacklist,bookmakers = user_bookmaker(blacklist=blacklist,bookmakers=bookmakers)
            case "2":           # Sets next_day to 0 to skip main scanning loop if no sports selected
                user_sports()
            case "C":
                pass
            case "E":
                user_settings_choice = "C"
                next_day = 0
            case _:
                clear_terminal()
                print("Please enter a valid input!")
                time.sleep(1)

# Initial screen with all options
clear_terminal()
start_interface()

if not user_urls:
    next_day = 0
else:
    # Initialize selenium scraper
    service = Service()
    options = webdriver.ChromeOptions()
    d = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(d,10)

# Scrape matches from every day until user decides to stop
while(next_day != 0):

    # Outputs which sports will be scanned
    clear_terminal()

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
                for x,value in enumerate(odds,0):
                    rolling_sum += (1/float(value))
                    odds[x] = float(value)              # Cast each odd from string to float

                # Calculates as a percentage of profit for user    
                rolling_sum = (1 - rolling_sum) * 100

                # Filter out blacklisted bookmakers from profitable bets
                if(any(x in site for x in blacklist) and rolling_sum >= 1 and rolling_sum != 0):
                    blocked_count += 1
                    rolling_sum = 0

                #Filters only profitable bets
                if(rolling_sum >= 1 and rolling_sum != 0):
                    count += 1
                    curr_bet = [status.text,odds,round(rolling_sum,2),link,site]
                    profit_bets.append(curr_bet)
                    print(f"[{len(profit_bets)}] {status.text} | Match: {*odds,} - Odds: {rolling_sum:.2f}%  -  {link} - Sites: {*site,}")
        
        # Display number of good bets and number of blacklisted bets
        if(count == 0):
            print(f"No good odds | Blocked: {blocked_count}")
        else:
            print(f"{count} Good Odds | Blocked: {blocked_count}")

    end_interface()
    print(next_day)

# RUN SELENIUM IN PARRALEL FOR EACH SPORT
# ADD OPTION TO ADD SPORTS BACK TO SELECTED
# CREATE A SETTINGS FILE TO STORE USER SETTINGS AND ADD NEW SPORTS TO THE LIST
# CLEAN UP SPAGHETTI OF ALL THESE INTERFACES INTERACTIONS, POSSIBLY LOOK INTO PYTHON GUI
# CALCULATOR FEATURE TO INPUT SPECIFIC AMOUNT I WANT ON A SINGLE ODD FOR A MATCH AND CALCULATES THE REST