
def calculate(odds: list,bet_amount: float) -> dict:
    '''Calculates how much to bet on each odd based on bet_amount
    Args:
        odds(list): List of all odds
        bet_amount(float): Total amount willing to bet

    Returns:
        unbiased_bet(dict): Amount to bet and profit for each odd ({odd: $ bet})
    '''

    unbiased_bet = {}   #Stores the amount to bet for each outcome for even profit
    
    for odd in odds:
        odd_cumulative = 0
        
        # Calculates the number to divide bet_amount by
        for odd2 in odds:
            odd_cumulative += odd / odd2
        initial_bet = bet_amount/odd_cumulative
        
        bet_outputs = round(initial_bet,2)

        unbiased_bet[odd] = bet_outputs

    return(unbiased_bet)

def calculate_remaining_bets(odds):

    print()
    for x,odd in enumerate(odds,1):
        print(f"[{x}] - {odd:.2f}")
    print("[C] - Close")
        
    odd_selected = input("Which odd are you betting on: ").upper()
    if odd_selected.isnumeric:
        if int(odd_selected) <= len(odds):
            odd_selected = odds[int(odd_selected)-1]
    else:
        return
    
    amount_bet = float(input(f"How much are you betting on {odd_selected}: "))

    value_multiplier = 0

    for odd1 in odds:
        value_multiplier += odd_selected / odd1
    total_bet = value_multiplier * amount_bet
def calculate_profit(bet: float, odd: float, total_bet: float) -> float:
    return round((bet * odd) - total_bet,2)

    print(f"You need to bet ${total_bet:.2f} in order to bet ${amount_bet} on {odd_selected}")
    # print_calc_results(calculate(odds=odds,bet_amount=total_bet),odds=odds)

# def is_float(string):
#     try:
#         float(string)
#         return True
#     except ValueError:
#         return False

# # Function for user to input odds and calculates if profit or not
# def input_odds():
#     odd_count = 1
#     odd_input = -1
#     odds = []

#     clear_terminal()
#     print("[C] - Exit")

#     while(odd_input != "C"):
#         odd_input = input(f"Enter odd #{odd_count}: ").upper()
#         if is_float(odd_input):
#             odds.append(float(odd_input))
#             odd_count += 1
#         else:
#             if odd_input != "C":
#                 print("\nEnter a valid input\n")
#         profit = get_profit(odds=odds)
#         
#     if profit > 0.0:
#         print(f"Profit of {profit}%")
#     else:
#         print(f"Not profitable bet ({profit}%)")

#     return odds

# Returns the profit of given odds
def get_profit(odds):
    rolling_count = 0

    for odd in odds:
        rolling_count += (1/float(odd))

    rolling_count = round(((1/rolling_count)-1) * 100,2)
    
    return rolling_count


# def print_calc_results(unbiased_bet,odds):
#     if unbiased_bet:
#         profit = get_profit(odds=odds)
#         keys = list(unbiased_bet.keys())
#         print("\nPlace following amount on respective odds:")
#         print(f"{'Odd':<10}{'Initial Bet':<15} Profit ({profit}%)")
#         print('-'*50)

#         for key in keys:
#             print(f"{key:<10}${unbiased_bet[key][0]:<15}${unbiased_bet[key][1]:<15}")


