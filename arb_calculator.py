
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


# Calculates rest of total bet based on amount bet on one odd
def calc_total_bet_needed(odds: list, odd_selected: float, amount_bet: float) -> tuple:
    value_multiplier = 0

    for odd in odds:
        value_multiplier += odd_selected / odd

    total_bet = round(value_multiplier * amount_bet,2)

    remaining_bet = total_bet - amount_bet
    odds.remove(odd_selected)
    other_odds = odds

    return remaining_bet, other_odds


def calculate_profit(bet: float, odd: float, total_bet: float) -> float:
    return round((bet * odd) - total_bet,2)


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


